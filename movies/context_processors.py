from .models import Category

def categories(request):
    """
    Add categories to context for all templates
    """
    return {
        'categories': Category.objects.all()
    }
