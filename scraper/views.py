import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .services.scraper import scrape_chapter


@csrf_exempt
def scrape_api(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=400)

    try:
        data = json.loads(request.body)
        url = data.get("url")

        content = scrape_chapter(url)

        return JsonResponse({
            "success": True,
            "content": content
        })

    except Exception as e:
        return JsonResponse({
            "success": False,
            "error": str(e)
        })

    return JsonResponse({
        "success": False,
        "error": "POST request required"
    })


from django.shortcuts import render
from .services.scraper import scrape_chapter


def scrape_view(request):

    content = None
    error = None

    if request.method == "POST":

        url = request.POST.get("url")

        try:
            content = scrape_chapter(url)

        except Exception as e:
            error = str(e)

    return render(
        request,
        "scraper/index.html",
        {
            "content": content,
            "error": error,
        }
    )
