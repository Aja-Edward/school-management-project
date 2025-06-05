# from rest_framework import viewsets
# from django_filters.rest_framework import DjangoFilterBackend

# from rest_framework.permissions import IsAuthenticated
# from .models import Timetable
# from .serializers import TimetableSerializer


# class TimetableViewSet(viewsets.ModelViewSet):
#     queryset = Timetable.objects.all()
#     serializer_class = TimetableSerializer
#     permission_classes = [IsAuthenticated]
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ["day", "section", "subject", "teacher"]  # Adjust as needed


# from rest_framework import viewsets, status
# from rest_framework.response import Response
# from rest_framework.decorators import action
# from django_filters.rest_framework import DjangoFilterBackend
# from .models import Timetable
# from .serializers import TimetableSerializer


# class TimetableViewSet(viewsets.ModelViewSet):
#     queryset = Timetable.objects.all()
#     serializer_class = TimetableSerializer
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ["day", "classroom", "teacher", "subject"]

#     @action(detail=False, methods=["post"], url_path="bulk-upload")
#     def bulk_upload(self, request):
#         """
#         Accept a list of timetable records in JSON and create them in bulk.
#         """
#         data = request.data

#         if not isinstance(data, list):
#             return Response(
#                 {"error": "Expected a list of timetable entries."}, status=400
#             )

#         serializer = self.get_serializer(data=data, many=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(
#                 {"message": "Bulk upload successful.", "count": len(serializer.data)},
#                 status=201,
#             )
#         return Response(serializer.errors, status=400)


import csv
import io
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from .models import Timetable
from .serializers import TimetableSerializer


class TimetableViewSet(viewsets.ModelViewSet):
    queryset = Timetable.objects.all()
    serializer_class = TimetableSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["day", "classroom", "teacher", "subject"]

    @action(detail=False, methods=["post"], url_path="bulk-upload")
    def bulk_upload(self, request):
        data = request.data
        if not isinstance(data, list):
            return Response(
                {"error": "Expected a list of timetable entries."}, status=400
            )
        serializer = self.get_serializer(data=data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Bulk upload successful.", "count": len(serializer.data)},
                status=201,
            )
        return Response(serializer.errors, status=400)

    @action(
        detail=False,
        methods=["post"],
        url_path="csv-upload",
        parser_classes=[MultiPartParser, FormParser],
    )
    def csv_upload(self, request):
        """
        Upload timetable data via CSV file.
        CSV columns must be: day,start_time,end_time,subject,teacher,classroom
        """
        file = request.FILES.get("file")
        if not file:
            return Response({"error": "No file uploaded."}, status=400)

        decoded_file = file.read().decode("utf-8")
        io_string = io.StringIO(decoded_file)
        reader = csv.DictReader(io_string)

        entries = []
        errors = []
        line_num = 1
        for row in reader:
            line_num += 1
            # Adjust field names according to your Timetable model fields
            entry_data = {
                "day": row.get("day"),
                "start_time": row.get("start_time"),
                "end_time": row.get("end_time"),
                "subject": row.get("subject"),
                "teacher": row.get("teacher"),
                "classroom": row.get("classroom"),
            }
            serializer = self.get_serializer(data=entry_data)
            if serializer.is_valid():
                entries.append(serializer)
            else:
                errors.append({"line": line_num, "errors": serializer.errors})

        if errors:
            return Response({"errors": errors}, status=400)

        # Save all valid entries
        for serializer in entries:
            serializer.save()

        return Response(
            {"message": f"CSV upload successful. {len(entries)} entries created."},
            status=201,
        )
