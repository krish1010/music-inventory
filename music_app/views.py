import smtplib
from collections import Counter
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

from .models import Music, Cart

cart = Cart([])


def init(request):
    cart.item_list.clear()
    return index(request)


def index(request):
    context = {
        'music_list': Music.objects.all(),
        'genre_set': get_all_genres(),
        'cart_list': set(cart.item_list)
    }
    return render(request, 'music_app/index.html', context)


def search(request):
    query = request.GET.get('name')
    music_list = Music.objects.filter(Q(name__icontains=query) | Q(genre__icontains=query) | Q(artist__icontains=query))
    context = {
        'music_list': music_list,
        'genre_set': get_all_genres(),
        'cart_list': set(cart.item_list)
    }
    return render(request, 'music_app/index.html', context)


def genre_view(request, genre):
    context = {
        'music_list': Music.objects.filter(genre=str(genre)),
        'genre_set': get_all_genres(),
        'cart_list': set(cart.item_list)
    }
    return render(request, 'music_app/index.html', context)


@login_required(login_url='/accounts/user_login/')
def add_to_cart(request, music_id):
    cart.item_list.append(get_object_or_404(Music, pk=music_id))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required(login_url='/accounts/user_login/')
def view_cart(request):
    cart_dict = {}
    cart.item_list.sort(key=lambda x: x.id)
    for item in cart.item_list:
        if item not in cart_dict:
            cart_dict[item] = 0
        cart_dict[item] += 1
    cart.total_price = 0
    cart.cal_total_price()
    context = {
        'cart_dict': cart_dict,
        'total_price': cart.total_price
    }
    return render(request, 'music_app/cart_details.html', context)


def increase_quantity(request, music_id):
    music = get_object_or_404(Music, pk=music_id)
    cart.item_list.append(music)
    return redirect('view_cart')


def decrease_quantity(request, music_id):
    music = get_object_or_404(Music, pk=music_id)
    cart.item_list.remove(music)
    return redirect('view_cart')


def get_all_genres():
    music_list = Music.objects.all()
    return set([music.genre for music in music_list])


def send_mail(request):
    list_tuples = [(k.name, v) for k, v in Counter(cart.item_list).items()]
    email_message = 'Hi ' + request.user.first_name + ',\n'
    for item in list_tuples:
        email_message += item[0] + ':' + str(item[1]) + '\n'
    email_message += 'Grand Total = Rs. ' + str(cart.total_price)
    print(email_message)

    email_sender = 'temp_music@outlook.com'
    email_recipient = request.user.email

    msg = MIMEMultipart()
    msg['From'] = email_sender
    msg['To'] = email_recipient
    msg['Subject'] = 'Billing information'

    msg.attach(MIMEText(email_message, 'plain'))

    # attachment_location = '{}'.format('C:\\Users\\Krish\\PycharmProjects\\MusicInventory\\music_app\\static\\music_app\\images' \
    #                       '\\alternative.jpg ')
    #
    # if attachment_location != '':
    #     filename = os.path.basename(attachment_location)
    #     attachment = open(attachment_location, "rb")
    #     part = MIMEBase('application', 'octet-stream')
    #     part.set_payload(attachment.read())
    #     encoders.encode_base64(part)
    #     part.add_header('Content-Disposition',
    #                     "attachment; filename= %s" % filename)
    #     msg.attach(part)

    try:
        server = smtplib.SMTP('smtp.office365.com', 587)
        server.ehlo()
        server.starttls()
        server.login(email_sender, 'harry_potter_pass')
        text = msg.as_string()
        server.sendmail(email_sender, email_recipient, text)
        print('email sent')
        server.quit()
    except:
        print("SMPT server connection error")

    return redirect('view_cart')


def clear_cart():
    cart.item_list.clear()
    cart_dict = {}
