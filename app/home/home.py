from bs4 import BeautifulSoup
from flask import Blueprint, render_template
from flask_login import current_user, login_user, logout_user
import requests
from app.models import Tovar
from app.main import korzina
from datetime import datetime


home_bp = Blueprint('home', __name__, template_folder='templates', static_folder='static')


def get_usd_exchange_rate():
    url = "https://cbr.ru/"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        usd_divs = soup.find_all('div', class_='col-md-2 col-xs-9 _right mono-num')

        if len(usd_divs) >= 4:

            return usd_divs[3].text.strip()
        else:
            return "Четвертый элемент не найден."
    else:
        return f"Ошибка при запросе страницы: {response.status_code}"



usd_rate = get_usd_exchange_rate()





@home_bp.route('/')
@home_bp.route('/index')
def index():
    korzin = korzina()
    tovar = Tovar.query.all()
    kolvo = len(korzin)
    current_time = datetime.now().strftime("%H:%M:")


    return render_template('home/index.html', tovars=tovar, korzina=kolvo, current_time=current_time, dollar_rate=usd_rate)
