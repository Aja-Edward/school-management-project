from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Attendance
from .serializers import AttendanceSerializer
from .filters import AttendanceFilter

import csv
from io import TextIOWrapper
from students.models import Student
from teacher.models import Teacher
from classroom.models import Section
from parent.models import ParentProfile


class AttendanceViewSet(viewsets.ModelViewSet):
    serializer_class = AttendanceSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = AttendanceFilter
    search_fields = ["student__first_name", "teacher__first_name"]
    ordering_fields = ["attendance_date", "student"]

    def get_queryset(self):
        user = self.request.user

        # If parent, restrict to only their children's attendance
        if user.is_authenticated and user.role == "parent":
            try:
                parent_profile = ParentProfile.objects.get(user=user)
                return Attendance.objects.filter(
                    student__in=parent_profile.children.all()
                )
            except ParentProfile.DoesNotExist:
                return Attendance.objects.none()

        # Other roles: return all
        return Attendance.objects.all()

    @action(detail=False, methods=["post"], url_path="import-csv")
    def import_csv(self, request):
        csv_file = request.FILES.get("file")
        if not csv_file:
            return Response(
                {"error": "No CSV file uploaded"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            decoded_file = TextIOWrapper(csv_file.file, encoding="utf-8")
            reader = csv.DictReader(decoded_file)

            for row in reader:
                student = Student.objects.get(id=row["student"])
                teacher = Teacher.objects.get(id=row["teacher"])
                section = Section.objects.get(id=row["section"])

                Attendance.objects.create(
                    student=student,
                    teacher=teacher,
                    section=section,
                    attendance_date=row["attendance_date"],
                    status=row["status"].lower(),
                )

            return Response(
                {"message": "CSV import successful."}, status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"], url_path="export-csv")
    def export_csv(self, request):
        response = Response(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="attendance.csv"'

        writer = csv.writer(response)
        writer.writerow(["student", "teacher", "section", "attendance_date", "status"])

        for record in self.filter_queryset(self.get_queryset()):
            writer.writerow(
                [
                    record.student.id,
                    record.teacher.id if record.teacher else "",
                    record.section.id,
                    record.attendance_date,
                    record.status,
                ]
            )

        return response
