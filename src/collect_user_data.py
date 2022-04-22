from bs4 import BeautifulSoup as bs


def collect_user_data(html) -> dict | None:

    bsHtml = bs(html, 'lxml')
    fio = user_info = country_and_city = tel = skype = soc_contacts = facebook = instagram = ''

    # Пробуем найти нужные нам данные, если их нет - пропускаем
    try:
        fio = bsHtml.find(class_='reviewer vcard').find(class_='fn').text
    except:
        return None # Если нет имени - страница удалена или что-то ещё

    try:
        user_info = bsHtml.find('div', {'style': 'width:100%; class='}).find('div')
    except:
        pass

    try:
        country_and_city = user_info.find_all('p')[1].text
        country_and_city = country_and_city[15:]
        country_and_city = country_and_city[:country_and_city.find('Зарегистрирован(а)')]
    except:
        pass

    try:
        tel = bsHtml.find('div', {'id': 'tel_contact'}).text[10:]
    except:
        pass

    try:
        skype = bsHtml.find('div', {'id': 'skype_contact'}).find('p').text
    except:
        pass

    try:
        soc_contacts = bsHtml.find('div', {'id': 'soc_contact'}).find('ul').find_all('li')
    except:
        pass

    if soc_contacts:
        for soc_contact in soc_contacts:
            soc_contact_text = soc_contact.text

            # Все пользователи по разному указывают ссылку на профиль(без https, www)
            # Чтобы собирать остальные ссылки(с ошибками) ищем фрагмент ссылки
            # который имеет наибольшый шанс встретиться, обрезаем и добавляем https://www.
            if 'facebook.com/' in soc_contact_text:
                facebook = soc_contact_text
                facebook = 'https://www.' + facebook[facebook.find('facebook.com/'):].strip()
                if facebook == 'https://www.facebook.com/':
                    facebook = '' # Если пользователь указал только домен фейсбука

            # Тоже что и выше
            if 'instagram.com/' in soc_contact_text:
                instagram = soc_contact_text
                instagram = 'https://www.' + instagram[instagram.find('instagram.com/'):].strip()
                if instagram == 'https://www.instagram.com/':
                    instagram = ''

    user_info = {
        'FIO': fio,
        'country_and_city': country_and_city,
        'tel': tel,
        'skype': skype,
        'instagram': instagram,
        'facebook': facebook
    }

    return user_info