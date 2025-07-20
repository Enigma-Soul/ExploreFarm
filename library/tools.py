from json import loads,dumps

class Tools:
    def __init__(self,lnk):
        self.lnk = lnk

        self.special_text = ["@","#","!"]


    # GET 系列
    def raw_type(self, type):
        return type.split(":")[0]

    def data(self,path):
        temp = self.lnk.read(path)["arguments"]
        if temp[0:2] == "ef":
            return self.decode(temp)
        else:
            return {}

    def nbt(self,path):
        return self.data(path)["nbt"]

    def seeds(self,data):
        return data["type"].split(":")[1]

    def type(self,path):
        return self.data(path)["type"]

    # json编码系列
    def decode(self,string):
        def count(str1,char):
            return str1.count(char)
        if count(string,self.special_text[0]) != 2:
            return None

        str2 = string.split(self.special_text[0])[1].split(self.special_text[0])[0]

        str2 = str2.replace(self.special_text[1]," ")
        str2 = str2.replace(self.special_text[2],"\"")


        return loads(str2)

    def encode(self,dictionary):
        def is_json(dict):
            return type(dict).__name__ == "dict"

        if not is_json(dictionary):
            return None

        str1 = dumps(dictionary,ensure_ascii=False,indent=None)

        str1 = str1.replace(" ", self.special_text[1])
        str1 = str1.replace("\"", self.special_text[2])
        str1 = str1.replace("\'", self.special_text[2])


        return f"@{str1}@"
