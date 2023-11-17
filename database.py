import json
import os

import dtime


class account:
    __data = {"account": {}}

    def __init__(self, file):
        self.file = file
        if os.path.exists(self.file):
            with open(self.file, "r") as f:
                self.__data = json.load(f)
        else:
            with open(self.file, "w") as f:
                json.dump(self.__data, f)

    def get_account(self, ID):
        mal = "👤 Bot foydalanuvchisi:\n"
        uz = self.__data["account"][str(ID)]["user"]
        mm = self.__data["account"][str(ID)]["mal"]
        mal += f"\nIsmi : {mm[0]}"
        mal += f"\nFamiliyasi : {mm[1]}"
        mal += f"\nProfil : @{uz}"
        mal += f"\n📞 Telefon raqami : @{mm[2]}"
        return mal

    def get_bot_soni(self) -> str:
        return f"Bot foydalanuvchilari soni {len(self.__data['account'])} ta"

    def get_full_name(self, ID) -> str:
        a = self.__data["account"][str(ID)]["mal"]
        return f"{a[1]} {a[0]}"

    def user_name_id(self, ID, name):
        self.__data["account"][str(ID)] = {
            "user": name
        }
        self.__savetojsonfile()

    def save_cod(self, ID, cod):
        try:
            l = self.__data["account"][str(ID)]["test"]
            l.append(cod)
            self.__savetojsonfile()
        except Exception:
            l = [cod]
            self.__data["account"][str(ID)]["test"] = l
            self.__savetojsonfile()

    def get_mal(self, ID) -> list:
        try:
            return self.__data["account"][str(ID)]["mal"]
        except Exception:
            return []

    def delet_cod(self, ID, cod) -> bool:
        dat = self.__data["account"][str(ID)]["test"][::-1]
        if cod <= len(dat):
            k = dat[cod - 1]
            del dat[cod - 1]
            self.__data["account"][str(ID)]["test"] = dat[::-1]
            tes.delet(str(k))
            self.__savetojsonfile()
            return True
        return False

    def set_mal(self, ID, mal: list):
        self.__data["account"][str(ID)]["mal"] = mal
        self.__savetojsonfile()

    def may_test(self, ID) -> str:
        try:
            mal = "Siz yaratgan testlar:"
            dat = self.__data["account"][str(ID)]["test"][::-1]
            k = 0
            if len(dat) != 0:
                for i in dat:
                    k += 1
                    a = tes.get_test_mal_full(str(i))
                    mal += f"\n\n🔠 {k}.{list(a['test'][0].keys())[0]}\n\tTestlar soni: {len(a['test'])}\n\tTest yaratilgan sana: {a['time']}\n\tTest codi: {str(i)}"
                mal += f"\n\nsiz yaratgan testlar soni: {len(dat)}"
                return mal
            else:
                return "😥 Siz hali test tuzmadingiz."
        except Exception:
            return "😥 Siz hali test tuzmadingiz."

    def __savetojsonfile(self):
        with open(self.file, "w") as f:
            json.dump(self.__data, f)


class test:
    __data = []

    def __init__(self, file):
        self.file = file
        if os.path.exists(self.file):
            with open(self.file, "r") as f:
                self.__data = json.load(f)
        else:
            with open(self.file, "w") as f:
                json.dump(self.__data, f)

    def savetest(self, ID, cod, t):
        di = {cod: {"id": ID, "time": dtime.hozirgi_vaqt(), "test": t}}
        self.__data.append(di)
        self.__savetojsonfile()

    def get_test_mal(self, cod) -> str:
        j = {}
        mal = ""
        k = -1
        for i in self.__data:
            k += 1
            s = list(i.keys())
            if cod in s:
                j = self.__data[k][str(cod)]
        if j == {}:
            return "none"
        else:
            user = ac.get_mal(j["id"])[1] + " " + ac.get_mal(j["id"])[0]
            mal += f"🔠 Test nomi: {list(j['test'][0].keys())[0]}\n👤 Test tuzuvch: {user}\n📅 Test tuzilgan sanasi: {j['time']}\nTestlar soni: {len(j['test'])}"
            return mal

    def cod_get(self, cod) -> bool:
        j = []
        for i in self.__data:
            j += list(i.keys())
        if cod in j:
            return True
        else:
            return False

    def delet(self, cod):
        k = -1
        try:
            for i in self.__data:
                k += 1
                if cod == str(list(i.keys())[0]):
                    del self.__data[k]
            self.__savetojsonfile()
        except Exception:
            self.__savetojsonfile()

    def get_test_mal_full(self, cod) -> dict:
        for i in self.__data:
            try:
                j = i[cod]
                return j
                break
            except Exception:
                continue
        return {}

    def get_cod(self) -> list:
        l = []
        for i in self.__data:
            k = list(i.keys())
            l += k
        return l

    def __savetojsonfile(self):
        with open(self.file, "w") as f:
            json.dump(self.__data, f)


class test_temp:
    __data = {"temp": {}}

    def __init__(self, file):
        self.file = file
        if os.path.exists(self.file):
            with open(self.file, "r") as f:
                self.__data = json.load(f)
        else:
            with open(self.file, "w") as f:
                json.dump(self.__data, f)

    def start(self, ID, name):
        self.__data["temp"][str(ID)] = {
            "name": name,
            "test": []
        }
        self.__savetojsonfile()

    def testvalue(self, ID) -> int:
        return len(self.__data["temp"][str(ID)]["test"])

    def get_test(self, ID) -> list:
        return self.__data["temp"][str(ID)]["test"]

    def delet(self, ID):
        a = self.__data["temp"][str(ID)]["test"]
        self.__data["temp"][str(ID)]["test"] = a[:len(a) - 1]
        self.__savetojsonfile()

    def set_test(self, ID, t: list):
        self.__data["temp"][str(ID)]["test"] = t
        self.__savetojsonfile()

    def get_test_name(self, ID):
        return self.__data["temp"][str(ID)]["name"]

    def __savetojsonfile(self):
        with open(self.file, "w") as f:
            json.dump(self.__data, f)


ac = account("Account.json")
tes = test("Test.json")
temp = test_temp("temp.json")
tes.delet("651")
