from django.db.models import Avg
from django.utils import timezone
from .models import Project, Testimonial

def get_portfolio_statistics():
    """
    Calculate and return portfolio statistics.
    """
    # Count published projects
    total_projects = Project.objects.filter(is_published=True).count()

    # Count unique clients
    unique_clients = Testimonial.objects.filter(is_published=True).values('client_name').distinct().count()

    # Calculate average satisfaction rate
    avg_rating = Testimonial.objects.filter(is_published=True).aggregate(
        avg=Avg('rating')
    )['avg'] or 0

    # Convert average rating (out of 5) to percentage
    satisfaction_rate = round((avg_rating / 5.0) * 100, 1) if avg_rating > 0 else 100

    # Calculate years of experience
    years_experience = 5  # Default value
    oldest_project = Project.objects.filter(
        is_published=True,
        completion_date__isnull=False
    ).order_by('completion_date').first()

    if oldest_project and oldest_project.completion_date:
        years_diff = (timezone.now().date() - oldest_project.completion_date).days / 365.25
        if years_diff > 0:
            years_experience = max(int(years_diff), 1)

    return {
        'total_projects': total_projects,
        'total_clients': unique_clients,
        'satisfaction_rate': satisfaction_rate,
        'years_experience': years_experience,
    }
