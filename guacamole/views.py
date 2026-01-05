from django.shortcuts import render, redirect
from django.http import JsonResponse
import requests
import logging

logger = logging.getLogger(__name__)

GUAC_BASE = "http://192.168.0.100:8090/guacamole/api"

def guac_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        logger.info(f"Próba logowania: {username}")

        try:
            # Wyślij login do API Guacamole
            res = requests.post(
                "http://192.168.0.100:8090/guacamole/api/tokens",
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                data={"username": username, "password": password}
            )
            logger.debug(f"Odpowiedź API: {res.status_code}, {res.text}")
            
            if res.status_code == 200:
                data = res.json()
                token = data.get("authToken")
                if not token:
                    logger.error(f"Brak tokenu w odpowiedzi: {data}")
                    return render(request, "guacamole/login.html", {"error": "Brak tokenu w odpowiedzi API."})

                # Zapisz token i login w sesji Django
                request.session['username'] = username
                request.session['auth_token'] = token

                logger.info(f"Logowanie zakończone sukcesem dla: {username}")
                return redirect('guac_session')  # widok sesji RDP/VNC
            else:
                logger.warning(f"Błąd logowania API: {res.status_code}")
                return render(request, "guacamole/login.html", {
                    "error": f"Błąd logowania: kod {res.status_code}"
                })
        except Exception as e:
            logger.exception("Wyjątek przy logowaniu do Guacamole")
            return render(request, "guacamole/login.html", {
                "error": f"Wyjątek: {str(e)}"
            })

    # GET – wyświetl formularz logowania
    return render(request, "guacamole/login.html")


def guac_session(request):
    token = request.session.get('auth_token')
    username = request.session.get('username')

    if not token:
        logger.info("Brak tokenu w sesji, przekierowanie na login")
        return redirect('guac_login')

    return render(request, "guacamole/session.html", {
        "username": username,
        "token": token,
    })


