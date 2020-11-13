#main Package
import json
import simplejson
import random
import pandas as pd
from flask import Flask, request, make_response, jsonify
from py2neo import Graph
from py2neo import Node
from py2neo import Relationship
from py2neo import ClientError
from pandas import DataFrame
import uuid

#Time
from datetime import date as tgl, timedelta
from time import localtime, strftime
from googletrans import Translator
tr = Translator()

uri = "bolt://127.0.0.1:7687"
user = "neo4j"
password = "secret"

app = Flask(__name__)
log = app.logger


@app.route('/webhook', methods=['POST'])
def webhook():

    #Neo4j permission
    g = Graph(uri=uri, user=user, password=password)

    #get request parameter
    req = request.get_json(force=True)
    action = req.get('queryResult').get('action')

    #check if request for action
    if action == 'input.welcome':

        name = req['originalDetectIntentRequest']['payload']['data']['from']
        user_id = name.get('id')
        id = str(user_id).split('.')[0]
        id = int(id)
        namadepan = name.get('first_name')
        namabelakang = name.get('last_name')

        mynode = list(g.nodes.match('UserTele', userid=id))

        if len(mynode) == 0:
            res = {
                'fulfillmentMessages': [{
                    "payload": {
                        "telegram": {
                            "text":
                            "<code>" + str(id) + "</code>" + "\nHai " +
                            namadepan + '\n' +
                            "Selamat datang di Informatics ᵇᵉᵗᵃ Chatbot",
                            "parse_mode":
                            "html"
                        }
                    },
                    "platform": "TELEGRAM"
                }, {
                    "payload": {
                        "telegram": {
                            "text":
                            "Anda belum terdaftar, silahkan klik Daftar untuk mendaftar!",
                            "reply_markup": {
                                "keyboard": [[{
                                    "text": "Daftar"
                                }]],
                                "resize_keyboard": True,
                                "one_time_keyboard": True
                            }
                        }
                    },
                    "platform": "TELEGRAM"
                }]
            }
        else:

            mynode = g.nodes.match('UserTele', userid=id).first()
            nama = mynode['namalengkap']

            res = {
                'fulfillmentMessages': [{
                    "payload": {
                        "telegram": {
                            "text": "Hai " + nama + '\n' +
                            "Selamat datang di Informatics ᵇᵉᵗᵃ Chatbot",
                            "reply_markup": {
                                "keyboard": [[{
                                    "text": "Menu"
                                }]],
                                "resize_keyboard": True,
                                "remove_keyboard": True
                            }
                        }
                    },
                    "platform": "TELEGRAM"
                }],
                'outputContexts':
                req['queryResult']['outputContexts']
            }

    if action == 'getDaftar':

        name = req['originalDetectIntentRequest']['payload']['data']['from']
        user_id = name.get('id')
        id = str(user_id).split('.')[0]
        id = int(id)

        mynode = list(g.nodes.match('UserTele', userid=id))

        if len(mynode) > 0:

            res = {
                'fulfillmentMessages': [{
                    "payload": {
                        "telegram": {
                            "text": "Anda sudah terdaftar!",
                            "parse_mode": "html"
                        }
                    },
                    "platform": "TELEGRAM"
                }],
                'outputContexts':
                req['queryResult']['outputContexts']
            }

        else:

            res = {
                'fulfillmentMessages': [{
                    "payload": {
                        "telegram": {
                            "reply_markup": {
                                "inline_keyboard": [[{
                                    "text": "Mahasiswa",
                                    "callback_data": "Mhs"
                                }],
                                                    [{
                                                        "callback_data":
                                                        "Dosen",
                                                        "text": "Dosen"
                                                    }]]
                            },
                            "text": "Pilih role anda.."
                        }
                    },
                    "platform": "TELEGRAM"
                }],
                'outputContexts':
                req['queryResult']['outputContexts']
            }

    if action == 'getDaftardosen':

        chat_id = req['originalDetectIntentRequest']['payload']['data']['callback_query']['message']['chat']
        chat_id = chat_id.get('id')
        message_id = req['originalDetectIntentRequest']['payload']['data']['callback_query']['message']
        message_id = message_id.get('message_id')
        message_id = str(message_id).split('.')[0]
        message_id = int(message_id) - 3
        id = req['originalDetectIntentRequest']['payload']['data']['callback_query']
        id = id.get('id')
        # message_id = message_id - 1

        res = {
            'fulfillmentMessages': [{
                "payload": {
                    "telegram": {
                        "text": "Fitur ini belum tersedia.",
                        "parse_mode": "html"
                    }
                },
                "platform": "TELEGRAM"
            },{
                "payload": {
                    "telegram": {
                        "text": "😢",
                        "parse_mode": "html"
                    }
                },
                "platform": "TELEGRAM"
            },{
                "payload": {
                    "telegram": {
                        "method": "deleteMessage",
                        "chat_id": chat_id,
                        "message_id": message_id
                        # "text": str(chat_id) + "\n" + str(message_id)
                    }
                },
                "platform": "TELEGRAM"
            },],
            'outputContexts':
            req['queryResult']['outputContexts']
        }

    if action == 'getDaftarmhs':

        param = req['originalDetectIntentRequest']['payload']['data']['from']
        username = param.get('username')
        first_name = param.get('first_name')
        last_name = param.get('last_name')
        user_id = param.get('id')
        id = str(user_id).split('.')[0]
        id = int(id)

        userparam = req['queryResult']['parameters']
        nama = userparam.get('nama')
        nama = nama.upper()
        email = userparam.get('email')
        prodi = userparam.get('prodi')
        angkatan = userparam.get('angkatan')
        angkatan = str(angkatan).split('.')[0]
        # angkatan = angkatan[-2:]
        angkatan = int(angkatan)
        veriv = userparam.get('veriv')

        if veriv == "no":

            res = {
                'fulfillmentMessages': [{
                    "payload": {
                        "telegram": {
                            "text": "Oke membatalkan!",
                            "parse_mode": "html"
                        }
                    },
                    "platform": "TELEGRAM"
                }, {
                    "quickReplies": {
                        "title": "kembali ke awal?",
                        "quickReplies": ["/start", "Sudah terima kasih"]
                    },
                    "platform": "TELEGRAM"
                }],
                'outputContexts':
                req['queryResult']['outputContexts']
            }

        else:

            if username is None:

                res = {
                    'fulfillmentMessages': [{
                        "payload": {
                            "telegram": {
                                "text":
                                "Harap lengkapi Username Telegram anda!",
                                "parse_mode": "html"
                            }
                        },
                        "platform": "TELEGRAM"
                    }],
                    'outputContexts':
                    req['queryResult']['outputContexts']
                }

            else:

                if len(str(angkatan)) < 4:

                    res = {
                        'fulfillmentMessages': [{
                            "payload": {
                                "telegram": {
                                    "text": "Angkatan harus niminmal 4 angka!",
                                    "parse_mode": "html"
                                }
                            },
                            "platform": "TELEGRAM"
                        }],
                        'outputContexts':
                        req['queryResult']['outputContexts']
                    }

                else:

                    node_email = g.nodes.match('UserTele', email=email).first()

                    if node_email is None:

                        query = g.run(
                            '''create (user:UserTele {userid: {uid}, username: {uname}, namalengkap: {namalengkap}, email: {email},
                                            prodi: {prodi}, angkatan: {angkatan}, role: "mahasiswa", pjkelas: "No"})''',
                            uid=id,
                            uname=username,
                            namalengkap=nama,
                            email=email,
                            prodi=prodi,
                            angkatan=angkatan)

                        res = {
                            'fulfillmentMessages': [{
                                "payload": {
                                    "telegram": {
                                        "text":
                                        "Nama : " + nama + "\nAngkatan : " +
                                        str(angkatan) + "\nProdi : " + prodi +
                                        "\nEmail : " + email +
                                        "\n\nTelah direcord di database\nTerima Kasih!",
                                        "parse_mode":
                                        "html"
                                    }
                                },
                                "platform": "TELEGRAM"
                            }],
                            'outputContexts':
                            req['queryResult']['outputContexts']
                        }

                    else:

                        res = {
                            'fulfillmentMessages': [{
                                "payload": {
                                    "telegram": {
                                        "text": "Email sudah terdaftar!",
                                        "parse_mode": "html"
                                    }
                                },
                                "platform": "TELEGRAM"
                            }],
                            'outputContexts':
                            req['queryResult']['outputContexts']
                        }

    if action == 'getMenu':

        name = req['originalDetectIntentRequest']['payload']['data']['from']
        user_id = name.get('id')
        id = str(user_id).split('.')[0]
        id = int(id)

        mynode = list(g.nodes.match('UserTele', userid=id))

        if len(mynode) == 0:
            res = {
                'fulfillmentMessages': [{
                    "payload": {
                        "telegram": {
                            "text":
                            "Anda belum terdaftar, silahkan klik Daftar untuk mendaftar!",
                            "reply_markup": {
                                "keyboard": [[{
                                    "text": "Daftar"
                                }]],
                                "resize_keyboard": True,
                                "one_time_keyboard": True
                            }
                        }
                    },
                    "platform": "TELEGRAM"
                }]
            }

        else:

            res = {
                'fulfillmentMessages': [{
                    "payload": {
                        "telegram": {
                            "text":
                            "<b>~Daftar Menu~</b>\n\n" +
                            "1. Lihat Mata Kuliah\n" +
                            "2. Lihat Mata Kuliah Spesifik\n" +
                            "3. Lihat ruang kelas yang tersedia\n" +
                            "4. Lihat rekomendasi ruang kelas pengganti\n" +
                            "5. Booking Ruang kelas pengganti\n" +
                            "6. Booking Ruang Sidang\n\n" +
                            "<code>*nb : jika tidak ada di pilihan, silahkan klik HELP untuk keyword</code>",
                            "parse_mode":
                            "html"
                        }
                    },
                    "platform": "TELEGRAM"
                }, {
                    "payload": {
                        "telegram": {
                            "text": "Silahkan memilih menu...",
                            "reply_markup": {
                                "keyboard":
                                [[{
                                    "text": "Lihat matkul"
                                }],
                                 [{
                                     "text": "Lihat ruang kelas yang tersedia"
                                 }], [{
                                     "text": "Help"
                                 }, {
                                     "text": "Tidak jadi!"
                                 }]],
                                "resize_keyboard":
                                True,
                                "one_time_keyboard":
                                True,
                                "remove_keyboard":
                                True
                            }
                        }
                    },
                    "platform": "TELEGRAM"
                }],
            }

    if action == 'usAvailableRuangKelas':

        name = req['originalDetectIntentRequest']['payload']['data']['from']
        user_id = name.get('id')
        id = str(user_id).split('.')[0]
        id = int(id)

        mynode = g.nodes.match('UserTele', userid=id).first()

        if mynode is None:

            res = {
                'fulfillmentMessages': [{
                    "payload": {
                        "telegram": {
                            "text":
                            "Anda belum terdaftar, silahkan klik Daftar untuk mendaftar!",
                            "reply_markup": {
                                "keyboard": [[{
                                    "text": "Daftar"
                                }]],
                                "resize_keyboard": True,
                                "one_time_keyboard": True
                            }
                        }
                    },
                    "platform": "TELEGRAM"
                }]
            }

        else:

            pj = mynode['pjkelas']

            if pj is 'No':

                res = {
                    'fulfillmentMessages': [{
                        "payload": {
                            "telegram": {
                                "text":
                                "Anda terdaftar bukan sebagai PJ Kelas, anda tidak bisa mengakses fitur ini!",
                                "reply_markup": {
                                    "keyboard": [[{
                                        "text": "Menu"
                                    }, {
                                        "text": "Tidak jadi!"
                                    }]],
                                    "resize_keyboard":
                                    True,
                                    "one_time_keyboard":
                                    True,
                                    "remove_keyboard":
                                    True
                                }
                            }
                        },
                        "platform": "TELEGRAM"
                    }]
                }

            else:

                res = {
                    'fulfillmentMessages': [{
                        "payload": {
                            "telegram": {
                                "reply_markup": {
                                    "inline_keyboard":
                                    [[{
                                        "callback_data": "Senin",
                                        "text": "Senin"
                                    }],
                                     [{
                                         "callback_data": "Selasa",
                                         "text": "Selasa"
                                     }],
                                     [{
                                         "callback_data": "Rabu",
                                         "text": "Rabu"
                                     }],
                                     [{
                                         "text": "Kamis",
                                         "callback_data": "Kamis"
                                     }],
                                     [{
                                         "text": "Jumat",
                                         "callback_data": "Jumat"
                                     }]]
                                },
                                "text": "Pilih hari..."
                            }
                        },
                        "platform": "TELEGRAM"
                    }],
                    'outputContexts':
                    req['queryResult']['outputContexts']
                }

    if action == 'getMenuMatkul':

        name = req['originalDetectIntentRequest']['payload']['data']['from']
        user_id = name.get('id')
        id = str(user_id).split('.')[0]
        id = int(id)

        mynode = g.nodes.match('UserTele', userid=id).first()

        if mynode is None:

            res = {
                'fulfillmentMessages': [{
                    "payload": {
                        "telegram": {
                            "text":
                            "Anda belum terdaftar, silahkan klik Daftar untuk mendaftar!",
                            "reply_markup": {
                                "keyboard": [[{
                                    "text": "Daftar"
                                }]],
                                "resize_keyboard": True,
                                "one_time_keyboard": True
                            }
                        }
                    },
                    "platform": "TELEGRAM"
                }]
            }

        else:

            res = {
                'fulfillmentMessages': [{
                    "text": {
                        "text": [
                            "Jika tidak ada di pilihan, silahkan ketik manual sesuai kelas anda. \nContoh : S1TI15"
                        ]
                    },
                    "platform": "TELEGRAM"
                }, {
                    "payload": {
                        "telegram": {
                            "text": "Silahkan memilih kelas...",
                            "reply_markup": {
                                "keyboard": [[{
                                    "text": "Sarjana Terapan 19B"
                                }, {
                                    "text": "Sarjana Terapan 19A"
                                }], [{
                                    "text": "S1TI19A"
                                }, {
                                    "text": "S1TI19B"
                                }]],
                                "resize_keyboard":
                                True,
                                "remove_keyboard":
                                True
                            }
                        }
                    },
                    "platform": "TELEGRAM"
                }],
                'outputContexts':
                req['queryResult']['outputContexts']
            }

    if action == 'getTidakJadi':

        # res = {'fulfillmentMessages': [
        #         {
        #           "payload": {
        #             "telegram": {
        #               "expectUserResponse": False,
        #               "text": "Sampai bertemu kembali!"
        #             }
        #           }
        #         }
        #         ]}
        res = {
            'fulfillmentMessages': [{
                "text": {
                    "text": ["Makasih ya, sampai ketemu lagi ... \U00002764"]
                },
                "platform": "TELEGRAM"
            }, {
                "text": {
                    "text": ["Nanti kalo tanya ketik 'Halo' aja ya..."]
                },
                "platform": "TELEGRAM"
            }]
        }

    if action == 'getGuideTimeslot':

        res = {
            'fulfillmentMessages': [{
                "text": {
                    "text": ["Berikut adalah informasi mengenai TimeSLot :\n"]
                },
                "platform": "TELEGRAM"
            }, {
                "text": {
                    "text": [
                        "Timeslot 1 = 7:00\n"
                        "Timeslot 2 = 7:50\n"
                        "Timeslot 3 = 8:40\n"
                        "Timeslot 4 = 9:30\n"
                        "Timeslot 5 = 10:20\n"
                        "Timeslot 6 = 11:10\n"
                        "Timeslot 7 = 13:00\n"
                        "Timeslot 8 = 13:50\n"
                        "Timeslot 9 = 14:40\n"
                        "Timeslot 10 = 15:30\n"
                        "Timeslot 11 = 16:20\n"
                        "TimeSLot 12 = 17:10"
                    ]
                },
                "platform": "TELEGRAM"
            }, {
                "quickReplies": {
                    "title": "Kembali ke Menu?",
                    "quickReplies": ["Menu"]
                },
                "platform": "TELEGRAM"
            }],
            'outputContexts':
            req['queryResult']['outputContexts']
        }

    if action == 'viewRuangSidang':

        name = req['originalDetectIntentRequest']['payload']['data']['from']
        user_id = name.get('id')
        id = str(user_id).split('.')[0]
        id = int(id)

        param = req['queryResult']['parameters']

        tanggal_param = param.get('date').split('T')[0]
        tanggal_covert = pd.to_datetime(tanggal_param)
        tanggal_day = tanggal_covert.strftime('%A')
        tanggal_day_tr = tr.translate(tanggal_day, dest='id', src='en')
        tanggal_month = tanggal_covert.strftime('%d-%B-%Y')
        tanggal_month_tr = tr.translate(tanggal_month, dest='id', src='en')
        tanggal = tanggal_day_tr.text + ',' + tanggal_month_tr.text

        query = pd.DataFrame(
            g.run(
                '''match (a:RuangSidang)-[r:BOOKING_AT]->(b:BookRuangSidang)<-[:BOOKED_BY]-(u:UserTele) 
          where r.status = 'booked' and b.tanggal = {t}
          return a.nama, b.acara, b.peserta, b.tanggal, b.jam, u.namalengkap''',
                t=tanggal))
        output = query.to_numpy()
        hasil = ''
        for row in output:
            hasil += f"Nama Ruang : {row[0]}\n"
            hasil += f"Judul Acara : {row[1]}\n"
            hasil += f"Nama Peserta : {row[2]}\n"
            hasil += f"Akan digunakan pada\n"
            hasil += f"Tanggal : {row[3]}\n"
            hasil += f"Jam : {row[4]}\n"
            hasil += f"Dibuat oleh : {row[5]}\n"
            hasil += f"\n"

        mynode = g.nodes.match('UserTele', userid=id).first()

        if mynode is None:

            res = {
                'fulfillmentMessages': [{
                    "payload": {
                        "telegram": {
                            "text":
                            "Anda belum terdaftar, silahkan klik Daftar untuk mendaftar!",
                            "reply_markup": {
                                "keyboard": [[{
                                    "text": "Daftar"
                                }]],
                                "resize_keyboard": True,
                                "one_time_keyboard": True
                            }
                        }
                    },
                    "platform": "TELEGRAM"
                }]
            }

        else:

            if output.size == 0:
                res = {
                    'fulfillmentMessages': [{
                        "text": {
                            "text": ["Belum Ada Pesanan!"]
                        },
                        "platform": "TELEGRAM"
                    }]
                }
            else:
                res = {
                    'fulfillmentMessages': [{
                        "text": {
                            "text": [
                                "DAFTAR RUANG SIDANG YANG AKAN DIPAKAI\n" +
                                "\n" + hasil
                            ]
                        },
                        "platform": "TELEGRAM"
                    }]
                }

    if action == 'bookRuangSidang':

        # id = uuid.uuid4().hex[:8]
        param = req['queryResult']['parameters']
        nama_param = req['originalDetectIntentRequest']['payload']['data'][
            'from']
        user_id = nama_param.get('id')
        id = str(user_id).split('.')[0]
        id = int(id)
        namadepan = nama_param.get('first_name')

        tanggal_param = param.get('date').split('T')[0]
        tanggal_covert = pd.to_datetime(tanggal_param)
        tanggal_day = tanggal_covert.strftime('%A')
        tanggal_day_tr = tr.translate(tanggal_day, dest='id', src='en')
        tanggal_month = tanggal_covert.strftime('%d-%B-%Y')
        tanggal_month_tr = tr.translate(tanggal_month, dest='id', src='en')
        tanggal = tanggal_day_tr.text + ',' + tanggal_month_tr.text

        time = param.get('time').split('T')[1].split('+')[0]
        ruang = param.get('ruangSidang')
        name = param.get('person')
        event = param.get('acara')
        date_time = tanggal_param + "/" + time
        code = ruang + date_time

        #timecreate
        today_ori = tgl.today()
        hariini = today_ori.strftime('%A')
        hariini = tr.translate(hariini, dest='id', src='en')
        today = today_ori.strftime('%d-%B-%Y')
        today = tr.translate(today, dest='id', src='en')
        waktu = strftime("%H:%M:%S", localtime())
        createat = hariini.text + ',' + today.text + '/' + waktu

        mynode = list(g.nodes.match('BookRuangSidang', kode=code))

        tod = pd.to_datetime(today_ori)
        yesterday = pd.to_datetime(tanggal_param)

        dosennode = g.nodes.match('UserTele', userid=id).first()

        if dosennode is None:

            res = {
                'fulfillmentMessages': [{
                    "payload": {
                        "telegram": {
                            "text":
                            "Anda belum terdaftar, silahkan klik Daftar untuk mendaftar!",
                            "reply_markup": {
                                "keyboard": [[{
                                    "text": "Daftar"
                                }]],
                                "resize_keyboard": True,
                                "one_time_keyboard": True
                            }
                        }
                    },
                    "platform": "TELEGRAM"
                }]
            }

        else:

            dosen = dosennode['role']

            if dosen == 'mahasiswa':
                res = {
                    'fulfillmentMessages': [{
                        "text": {
                            "text": [
                                "Maaf anda bukan dosen, anda tidak bisa mengakses fitur ini!"
                            ]
                        },
                        "platform": "TELEGRAM"
                    }]
                }

            else:

                if yesterday < tod:
                    res = {
                        'fulfillmentMessages': [{
                            "text": {
                                "text": ["Tidak bisa pesan!"]
                            },
                            "platform": "TELEGRAM"
                        }, {
                            "text": {
                                "text": [
                                    "Tidak bisa mememesan ruang sebelum hari ini."
                                ]
                            },
                            "platform": "TELEGRAM"
                        }]
                    }

                else:

                    if len(mynode) > 0:
                        res = {
                            'fulfillmentMessages': [{
                                "text": {
                                    "text": ["Sudah DIpesan!!"]
                                },
                                "platform": "TELEGRAM"
                            }]
                        }

                    else:

                        result = g.run('''match (rs:RuangSidang) 
                          match (user:UserTele)
                          where rs.nama = {rs} and user.userid = {id} 
                          create (brs:BookRuangSidang {kode: {x}, tanggal: {t}, jam: {j}, acara: {a}, peserta: {p}, createat: {c}}) 
                          create (rs)-[:BOOKING_AT {status: 'booked'}]->(brs)<-[:BOOKED_BY]-(user)''',
                                       id=id,
                                       x=code,
                                       t=tanggal,
                                       j=time,
                                       rs=ruang,
                                       c=createat,
                                       a=event,
                                       p=name)
                        res = {
                            'fulfillmentMessages': [{
                                "text": {
                                    "text": ["Berhasil di set!"]
                                },
                                "platform": "TELEGRAM"
                            }, {
                                "text": {
                                    "text": [
                                        ruang + " dipesan pada tanggal " +
                                        tanggal + " jam " + time + '\n' +
                                        'Dibuat pada: ' + createat +
                                        '\nDibuat oleh : ' + namadepan
                                    ]
                                },
                                "platform": "TELEGRAM"
                            }]
                        }

    if action == 'viewAllRuangSidang':

        nama_param = req['originalDetectIntentRequest']['payload']['data'][
            'from']
        user_id = nama_param.get('id')
        id = str(user_id).split('.')[0]
        id = int(id)

        query = pd.DataFrame(
            g.run(
                "match (a:RuangSidang)-[r:BOOKING_AT]->(b:BookRuangSidang) where r.status = 'booked' return a.nama, b.acara, b.peserta, b.tanggal, b.jam"
            ))
        output = query.to_numpy()
        hasil = ''
        for row in output:
            hasil += f"Nama Ruang : {row[0]}\n"
            hasil += f"Judul Acara : {row[1]}\n"
            hasil += f"Nama Peserta : {row[2]}\n"
            hasil += f"Akan digunakan pada\n"
            hasil += f"Tanggal : {row[3]}\n"
            hasil += f"Jam : {row[4]}\n"
            hasil += f"\n"

        mynode = g.nodes.match('UserTele', userid=id).first()

        if mynode is None:

            res = {
                'fulfillmentMessages': [{
                    "payload": {
                        "telegram": {
                            "text":
                            "Anda belum terdaftar, silahkan klik Daftar untuk mendaftar!",
                            "reply_markup": {
                                "keyboard": [[{
                                    "text": "Daftar"
                                }]],
                                "resize_keyboard": True,
                                "one_time_keyboard": True
                            }
                        }
                    },
                    "platform": "TELEGRAM"
                }]
            }

        else:

            if output.size == 0:
                res = {
                    'fulfillmentMessages': [{
                        "text": {
                            "text": ["Belum Ada Pesanan!"]
                        },
                        "platform": "TELEGRAM"
                    }]
                }
            else:
                res = {
                    'fulfillmentMessages': [{
                        "text": {
                            "text": [
                                "DAFTAR RUANG SIDANG YANG AKAN DIPAKAI\n" +
                                "\n" + hasil
                            ]
                        },
                        "platform": "TELEGRAM"
                    }]
                }

    if action == 'deleteRuangSidang':

        nama_param = req['originalDetectIntentRequest']['payload']['data'][
            'from']
        user_id = nama_param.get('id')
        id = str(user_id).split('.')[0]
        id = int(id)
        namadepan = nama_param.get('first_name')

        param = req['queryResult']['parameters']
        tanggal_param = param.get('date').split('T')[0]
        tanggal_covert = pd.to_datetime(tanggal_param)
        tanggal_day = tanggal_covert.strftime('%A')
        tanggal_day_tr = tr.translate(tanggal_day, dest='id', src='en')
        tanggal_month = tanggal_covert.strftime('%d-%B-%Y')
        tanggal_month_tr = tr.translate(tanggal_month, dest='id', src='en')
        date = tanggal_day_tr.text + ',' + tanggal_month_tr.text
        time = param.get('time').split('T')[1].split('+')[0]
        ruang = param.get('ruangSidang')
        # tanggal = date + "/" + time

        #timecreate
        today_ori = tgl.today()
        hariini = today_ori.strftime('%A')
        hariini = tr.translate(hariini, dest='id', src='en')
        today = today_ori.strftime('%d-%B-%Y')
        today = tr.translate(today, dest='id', src='en')
        waktu = strftime("%H:%M:%S", localtime())
        updateat = hariini.text + ',' + today.text + '/' + waktu

        query = list(
            g.run('''match (a:RuangSidang)-[r:BOOKING_AT]->(b:BookRuangSidang)
          match (user:UserTele) 
          where a.nama = {rs} and b.tanggal = {t} and b.jam = {j} and user.userid = {id}
          set b:HistoryRuangSidang, r.status = 'history', b.updateat = {u}
          create (b)<-[:DELETED_BY]-(user)
          ''',
                  rs=ruang,
                  t=date,
                  j=time,
                  u=updateat,
                  id=id))

        if len(query) == 0:
            res = {
                'fulfillmentMessages': [{
                    "text": {
                        "text": ["Gagal Menghapus!"]
                    },
                    "platform": "TELEGRAM"
                }],
                'outputContexts':
                req['queryResult']['outputContexts']
            }
        else:
            res = {
                'fulfillmentMessages': [{
                    "text": {
                        "text": ["Berhasil Dihapus!"]
                    },
                    "platform": "TELEGRAM"
                }],
                'outputContexts':
                req['queryResult']['outputContexts']
            }

    # else :
    #     # If the request is not to the action throw an error
    #     log.error('Unexpected action requested: %s', json.dumps(req))
    #     res = {'speech': 'error', 'displayText': 'error'}

    if action == 'getHistoryRuangSidang':

        param = req['queryResult']['parameters']
        tanggal_param = param.get('date').split('T')[0]
        tanggal_covert = pd.to_datetime(tanggal_param)
        tanggal_day = tanggal_covert.strftime('%A')
        tanggal_day_tr = tr.translate(tanggal_day, dest='id', src='en')
        tanggal_month = tanggal_covert.strftime('%d-%B-%Y')
        tanggal_month_tr = tr.translate(tanggal_month, dest='id', src='en')
        tanggal = tanggal_day_tr.text + ',' + tanggal_month_tr.text

        query = pd.DataFrame(
            g.run(
                '''match (a:RuangSidang)-[r:BOOKING_AT]->(b:HistoryRuangSidang)<-[:DELETED_BY]-(u:UserTele) 
          match (a:RuangSidang)-[r:BOOKING_AT]->(b:HistoryRuangSidang)<-[:BOOKED_BY]-(us:UserTele)
          where r.status = 'history' and b.tanggal = {t} 
          return a.nama, b.acara, b.peserta, b.tanggal, us.namalengkap, b.updateat, u.namalengkap''',
                t=tanggal))
        output = query.to_numpy()
        hasil = ''
        for row in output:
            hasil += f"Nama Ruang : {row[0]}\n"
            hasil += f"Judul Acara : {row[1]}\n"
            hasil += f"Nama Peserta : {row[2]}\n"
            hasil += f"Tanggal/Jam : {row[3]}\n"
            hasil += f"Dibuat oleh : {row[4]}\n\n"
            hasil += f"Dihapus pada : {row[5]}\n"
            hasil += f"Oleh : {row[6]}\n___________________________"
            hasil += f"\n"

        if output.size == 0:
            res = {
                'fulfillmentMessages': [{
                    "text": {
                        "text": ["Belum Ada History Pemesanan!"]
                    },
                    "platform": "TELEGRAM"
                }],
                'outputContexts':
                req['queryResult']['outputContexts']
            }
        else:
            res = {
                'fulfillmentMessages': [{
                    "text": {
                        "text": [
                            "DAFTAR HISTORY PESANAN RUANG SIDANG\nPADA " +
                            tanggal + "\n\n" + hasil
                        ]
                    },
                    "platform": "TELEGRAM"
                }],
                'outputContexts':
                req['queryResult']['outputContexts']
            }

    if action == 'viewJadwalSpecificOri':

        param = req['queryResult']['parameters']
        kelas = param.get('Kelas')
        matkul = param.get('matkul')

        query = pd.DataFrame(
            g.run('''match (dosen:Dosen)-[:MENGAJAR]->(matkul:Matkul)
            match (kelas:Kelas)-[:BELAJAR]->(matkul:Matkul)-[:HAS_DAY]-(hari:Hari) 
            match (kelas:Kelas)-[:BELAJAR]->(matkul:Matkul)-[:HAS_ROOM]-(ruang:Ruang) 
            match (kelas:Kelas)-[:BELAJAR]->(matkul:Matkul)-[:HAS_TIME]-(jam:TimeSlot) 
            where kelas.nama = {x} and matkul.nama = {z} 
            return kelas.nama as Kelas, matkul.nama as Matkul, matkul.sks as Sks, dosen.nama as Dosen, ruang.nama as Ruang, hari.nama as Hari, jam.jam as Jam''',
                  x=kelas,
                  z=matkul))
        query = query.to_numpy()
        hasil = ''
        for row in query:
            hasil += f"Kelas : {row[0]}\n"
            hasil += f"Matkul : {row[1]}\n"
            hasil += f"Sks : {row[2]}\n"
            hasil += f"Dosen : {row[3]}\n"
            hasil += f"Ruang : {row[4]}\n"
            hasil += f"Hari : {row[5]}\n"
            hasil += f"Jam : {row[6]}\n"
            hasil += f"\n"

        if len(query) == 0:
            res = {
                "fulfillmentMessages": [{
                    "payload": {
                        "telegram": {
                            "text": "Kosong!"
                        }
                    },
                    "platform": "TELEGRAM"
                }, {
                    "quickReplies": {
                        "title": "kembali ke Menu?",
                        "quickReplies": ["Menu", "Sudah terima kasih"]
                    },
                    "platform": "TELEGRAM"
                }],
                'outputContexts':
                req['queryResult']['outputContexts']
            }
        else:
            res = {
                "fulfillmentMessages": [{
                    "payload": {
                        "telegram": {
                            "text":
                            " \U00002b50 JADWAL MATAKULIAH " + matkul.upper() +
                            " ADALAH \U00002b50 \n\n " + hasil
                        }
                    },
                    "platform": "TELEGRAM"
                }, {
                    "quickReplies": {
                        "title": "kembali ke Menu?",
                        "quickReplies": ["Menu", "Sudah terima kasih"]
                    },
                    "platform": "TELEGRAM"
                }],
                'outputContexts':
                req['queryResult']['outputContexts']
            }

    if action == 'getViewMatkul':

        getViewMatkul = req['queryResult']['parameters']

        matkul = getViewMatkul.get('Kelas')

        data1 = req['originalDetectIntentRequest']['payload']['data']['from']
        chat_id = data1.get('chat_id')
        data2 = req['originalDetectIntentRequest']['payload']['data']
        message_id = data2.get('message_id')

        mat = pd.DataFrame(
            g.run(
                "match (kelas:Kelas)-[:BELAJAR]->(matkul:Matkul)-[:HAS_ROOM]->(ruang:Ruang) match (kelas:Kelas)-[:BELAJAR]->(matkul:Matkul)-[:HAS_DAY]->(hari:Hari) match (kelas:Kelas)-[:BELAJAR]->(matkul:Matkul)-[:HAS_TIME]->(jam:TimeSlot) match (kelas:Kelas)-[:BELAJAR]->(matkul:Matkul)<-[:MENGAJAR]-(dosen:Dosen) where kelas.nama = {x} return kelas.nama, matkul.nama, matkul.sks, dosen.nama, ruang.nama, hari.nama, jam.jam order by hari.nama desc",
                x=matkul))
        mat = mat.to_numpy()
        hasil = ''
        for row in mat:
            hasil += f"Kelas : {row[0]}\n"
            hasil += f"Matkul : {row[1]}\n"
            hasil += f"Sks : {row[2]}\n"
            hasil += f"Dosen : {row[3]}\n"
            hasil += f"Ruang : {row[4]}\n"
            hasil += f"Hari : {row[5]}\n"
            hasil += f"Jam : {row[6]}\n"
            hasil += f"\n"

        if len(mat) == 0:
            res = {
                "fulfillmentMessages": [{
                    "payload": {
                        "telegram": {
                            "text":
                            "Tidak ditemukan matkul untuk kelas tersebut!"
                        }
                    },
                    "platform": "TELEGRAM"
                }, {
                    "quickReplies": {
                        "title": "kembali ke Menu?",
                        "quickReplies": ["Menu", "Sudah terima kasih"]
                    },
                    "platform": "TELEGRAM"
                }],
                'outputContexts':
                req['queryResult']['outputContexts']
            }
        else:
            res = {
                "fulfillmentMessages": [{
                    "payload": {
                        "telegram": {
                            "text":
                            " \U00002b50 JADWAL MATAKULIAH " + matkul.upper() +
                            " ADALAH \U00002b50 \n\n " + hasil
                        }
                    },
                    "platform": "TELEGRAM"
                }, {
                    "payload": {
                        "telegram": {
                            "text": "Ingin kembali ke menu?",
                            "reply_markup": {
                                "keyboard": [[{
                                    "text": "Menu"
                                }, {
                                    "text": "Sudah Terima Kasih"
                                }]],
                                "resize_keyboard":
                                True,
                                "one_time_keyboard":
                                True
                            }
                        }
                    },
                    "platform": "TELEGRAM"
                }],
                'outputContexts':
                req['queryResult']['outputContexts']
            }

    if action == 'getAvailableRuangKelas':

        get = req['queryResult']['parameters']
        hari = get.get('date-time')

        mat = pd.DataFrame(
            g.run(
                "match (kelas:Kelas)-[:BELAJAR]->(matkul:Matkul)-[:HAS_ROOM]->(ruang:Ruang) match (kelas:Kelas)-[:BELAJAR]->(matkul:Matkul)-[:HAS_DAY]->(hari:Hari) match (kelas:Kelas)-[:BELAJAR]->(matkul:Matkul)-[:HAS_TIME]->(jam:TimeSlot) match (kelas:Kelas)-[:BELAJAR]->(matkul:Matkul)<-[:MENGAJAR]-(dosen:Dosen) where hari.nama = {x} return kelas.nama, matkul.nama, matkul.sks, ruang.nama, hari.nama, jam.jam order by hari.nama desc",
                x=hari))
        mat = mat.to_numpy()
        mat = [{
            'kelas': d[0],
            'matkul': d[1],
            'sks': d[2],
            'ruangan': d[3],
            'start': d[-1]
        } for d in mat]
        for row in mat:
            exploded = row['start'].split(':')
            start = (int(exploded[0]) * 60) + int(exploded[1])
            row['start'] = start
            row['end'] = start + (row['sks'] * 50)

        ruangan = pd.DataFrame(
            g.run("match (ruang:Ruang) return ruang.nama order by ruang.nama"))
        ruangan = [r[0] for r in ruangan.to_numpy()]

        kelas_mulai = 7 * 60
        kelas_selesai = (18 * 60)
        istirahat_mulai = (12 * 60)
        istirahat_selesai = (13 * 60)

        ruangan_timeslots = {}
        for r in ruangan:
            _data = [d for d in mat if d['ruangan'] == r]

            timeslots = {
                ts: True
                for ts in range(kelas_mulai, kelas_selesai + 1)
            }

            for ts in range(istirahat_mulai, istirahat_selesai + 1):
                timeslots[ts] = False

            for row in _data:
                for ts in range(row['start'], row['end'] + 1):
                    timeslots[ts] = False

            timeslots = [key for key in timeslots if timeslots[key]]
            start_flag = timeslots[0]
            _availables = []
            for c in range(1, len(timeslots)):
                if timeslots[c] - 1 != timeslots[c - 1]:
                    _availables.append({
                        'start': start_flag,
                        'end': timeslots[c - 1]
                    })
                    start_flag = timeslots[c]

                if c == len(timeslots) - 1:
                    _availables.append({
                        'start': start_flag,
                        'end': timeslots[c]
                    })

            def jam(menit):
                sisa = menit % 60
                jam = int((menit - sisa) / 60)
                return f'{jam}:{sisa:02d}'

            availables = []
            for av in _availables:
                start = jam(av['start'])
                end = jam(av['end'])
                availables.append(f'{start} - {end}')

            ruangan_timeslots[r] = availables

        hasil = ''
        for key in ruangan_timeslots:
            if len(ruangan_timeslots[key]) > 0:
                hasil += f' \U00002714 Ruang {key}\n'
                for jam in ruangan_timeslots[key]:
                    hasil += f'Jam : {jam}\n'
                hasil += '\n'

        res = {
            "fulfillmentMessages": [{
                "payload": {
                    "telegram": {
                        "text":
                        "\U00002b50 RUANGAN YANG TERSEDIA PADA HARI " +
                        hari.upper() + " ADALAH \U00002b50\n\n\n" + hasil
                    }
                },
                "platform": "TELEGRAM"
            }, {
                "quickReplies": {
                    "title": "kembali ke Menu?",
                    "quickReplies": ["Menu", "Sudah terima kasih"]
                },
                "platform": "TELEGRAM"
            }],
            'outputContexts':
            req['queryResult']['outputContexts']
        }

    if action == 'availableRuangKelasSpecific':

        param = req['queryResult']['parameters']
        kelas = param.get('Kelas')
        matkul = param.get('matkul')

        query = pd.DataFrame(
            g.run(
                "load csv with headers from 'file:///datadump.csv' as row with row where row.Kode = {z} and row.Kelas = {x} return row.Kelas as Kelas, row.Kode as Matkul, row.Sks as SKS, row.Ruang as Ruang, row.Hari as Hari, row.Jam as Jam order by row.Kelas, row.Hari desc",
                x=kelas,
                z=matkul))
        query = query.to_numpy()
        hasil = ''
        for row in query:
            hasil += f"Kelas : {row[0]}\n"
            hasil += f"Matkul : {row[1]}\n"
            hasil += f"Sks : {row[2]}\n"
            hasil += f"Ruang : {row[3]}\n"
            hasil += f"Hari : {row[4]}\n"
            hasil += f"Jam : {row[5]}\n"
            hasil += f"\n"

        res = {
            "fulfillmentMessages": [{
                "payload": {
                    "telegram": {
                        "text":
                        " \U00002b50 REKOMENDASI RUANGAN KULIAH ADALAH \U00002b50 \n\n "
                        + hasil
                    }
                },
                "platform": "TELEGRAM"
            }, {
                "quickReplies": {
                    "title": "kembali ke Menu?",
                    "quickReplies": ["Menu", "Sudah terima kasih"]
                },
                "platform": "TELEGRAM"
            }],
            'outputContexts':
            req['queryResult']['outputContexts']
        }

    if action == 'bookRuangKelas':

        id = uuid.uuid4().hex[:8]
        param = req['queryResult']['parameters']
        date = param.get('date').split('T')[0]
        time = param.get('time').split('T')[1].split('+')[0]
        ruang = param.get('ruang')
        kelas = param.get('kelas')
        matkul = param.get('matkul')
        tanggal = date + "/" + time

        hasil = g.run(
            "match (kelas:Kelas)-[:BELAJAR]->(matkul:Matkul)-[:HAS_ROOM]->(rk:Ruang) where kelas.nama = {k} and matkul.nama = {m} and rk.nama = {rk} create (brk:BookRuangKelas {kode: {x}, tanggal: {z}}) create (rk)-[:BOOKING_AT]->(brs)",
            k=kelas,
            m=matkul,
            x=id,
            z=tanggal,
            rk=ruang)

        res = {
            'fulfillmentMessages': [{
                "text": {
                    "text": ["Berhasil di set!"]
                },
                "platform": "TELEGRAM"
            }, {
                "text": {
                    "text": [
                        str(matkul) + " " + str(kelas) + " " + " diganti ke " +
                        ruang + " pada tanggal " + date + " jam " + time
                    ]
                },
                "platform": "TELEGRAM"
            }],
            'outputContexts':
            req['queryResult']['outputContexts']
        }

    if action == 'viewBookRuangKelas':

        output = pd.DataFrame(
            g.run(
                "match (kelas:Kelas)-[:BELAJAR]->(matkul:Matkul)-[:HAS_ROOM]->(rk:Ruang)-[:BOOKING_AT]->(b:BookRuangKelas) return kelas.nama, matkul.nama, rk.nama, b.tanggal"
            ))
        output = output.to_numpy()
        hasil = ''
        for row in output:
            hasil += f"Nama Kelas : {row[0]}\n"
            hasil += f"Matkul : {row[1]}\n"
            hasil += f"Ruang : {row[2]}\n"
            hasil += f"Tanggal : {row[3]}\n"
            hasil += f"\n"

        res = {
            'fulfillmentMessages': [{
                "text": {
                    "text": ["Data Perubahan Ruangan Matakuliah :\n"]
                },
                "platform": "TELEGRAM"
            }, {
                "text": {
                    "text": [hasil]
                },
                "platform": "TELEGRAM"
            }],
            'outputContexts':
            req['queryResult']['outputContexts']
        }

    return make_response(jsonify(res))


if __name__ == '__main__':
    PORT = 5000

    app.run(debug=True, port=PORT, host='0.0.0.0')