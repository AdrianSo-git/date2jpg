from PIL import ImageFont, ImageDraw
import PIL
import datetime
import os
import tkinter
from tkinter import filedialog, messagebox

class Application:

    def __init__(self):

        self.date_font = ImageFont.truetype('./conf/OpenSans-Bold.ttf', 150) # ustawienie czcionki dla daty

        self.okno = tkinter.Tk()  # tworzenie okna głównego
        self.okno.geometry("600x200") # ustawienie wymiarów okna
        self.okno.title("Date2JPG")  # ustawienie tytułu okna głównego

        self.naglowek = tkinter.Label(self.okno, text = "Program nanosi na zdjęcie datę wyciągniętą z jego EXIF.\n"
                                                        "Zdjęcia są pobierane z katalogu źródłowego i po naniesieniu\n"
                                                        "daty zapisywane w katalogu docelowym.\n")
        self.naglowek.pack()

        self.kz = os.getcwd()  # katalog źródłowy
        self.kd = os.getcwd()  # katalog docelowy

        self.ramka1 = tkinter.Frame(self.okno)
        self.ramka1.pack(fill=tkinter.BOTH, expand=True)

        self.wkz_button = tkinter.Button(self.ramka1, width=20, text="Wybierz katalog źródłowy:",
                                    command=self.wybierz_katalog_zrodlowy)
        self.wkz_button.pack(side=tkinter.LEFT)
        self.wkz_label = tkinter.Label(self.ramka1, text=self.kz)
        self.wkz_label.pack(side=tkinter.LEFT)

        self.ramka2 = tkinter.Frame(self.okno)
        self.ramka2.pack(fill=tkinter.BOTH, expand=True)

        self.wkd_button = tkinter.Button(self.ramka2, width=20, text="Wybierz katalog docelowy:",
                                    command=self.wybierz_katalog_docelowy)
        self.wkd_button.pack(side=tkinter.LEFT)

        self.wkd_label = tkinter.Label(self.ramka2, text=self.kd)
        self.wkd_label.pack(side=tkinter.LEFT)

        self.ramka3 = tkinter.Frame(self.okno)
        self.ramka3.pack(fill=tkinter.BOTH, expand=True)

        self.uruchom_button = tkinter.Button(self.ramka3, width=20, text="Uruchom!",
                                    command=self.wykonaj_dzialania)
        self.uruchom_button.pack(side=tkinter.LEFT)

        self.uruchom_label = tkinter.Label(self.ramka3, text="")
        self.uruchom_label.pack(side=tkinter.LEFT)

        self.etykieta = tkinter.Label(self.okno, text="by AdrianSo")
        self.etykieta.pack()

        self.okno.mainloop()

    def wybierz_katalog_zrodlowy(self):

        katalog = tkinter.filedialog.askdirectory()
        if katalog:
            self.kz = katalog
            self.wkz_label.configure(text=self.kz)

    def wybierz_katalog_docelowy(self):

        katalog = tkinter.filedialog.askdirectory()
        if katalog:
            self.kd = katalog
            self.wkd_label.configure(text=self.kd)

    def wykonaj_dzialania(self):

        if self.kd == self.kz:
            tkinter.messagebox.showinfo("Info", "Katalog docelowy musi być inny niż źródłowy.")  # info o błędzie
            return
        else:
            lista = list(os.listdir(self.kz))
            lista.sort()
            for i in lista:
                if os.path.isfile("{}/{}".format(self.kz,i)) and os.path.splitext(i)[1].upper()[1:] == "JPG":
                    self.uruchom_label.configure(text = "Przetwarzam {}".format(i))
                    self.uruchom_label.update_idletasks()
                    self.date2img(i)
                self.uruchom_label.configure(text = "Skończyłem przetwarzać")

    def date2img(self,i):

        # otwieranie zdjęcia i konwertowanie do RGBA

        self.img = PIL.Image.open("{}/{}".format(self.kz,i)).convert("RGBA")

        # wyciąganie daty z EXIF zdjęcia i formatowanie jej

        self.img_exif = dict(self.img.getexif())
        self.img_date = str(self.img_exif[36867])
        self.img_date_obj = datetime.datetime.strptime(self.img_date, "%Y:%m:%d %H:%M:%S")
        self.img_date_obj = self.img_date_obj.strftime("%d-%m-%Y")

        # tworzenie obrazu z datą

        self.img_text = PIL.Image.new('RGBA', self.img.size, (255, 255, 255, 0))
        self.img_text_draw = PIL.ImageDraw.Draw(self.img_text)
        self.img_text_draw.text(
            (self.img.size[0] - 1000,
            self.img.size[1] - 300),
            self.img_date_obj,
            font=self.date_font,
            fill=(255, 255, 255, 255)
        )

        # łączenie zdjęcia z obrazem z datą i konwertowanie do RGB

        self.img_with_date = PIL.Image.alpha_composite(self.img, self.img_text).convert("RGB")

        # zapisywanie zdjęcia z datą

        self.img_with_date.save("{}/{}".format(self.kd,i), quality=98)


app = Application()