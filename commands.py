import serpapi as api

class Status:
    def __init__(self):
        self.running = True
        self.active = True
        self.state = "Listening"
        self.perms = self.Permissions()

    def detectCommands(self, text):
        print(text)
        words = text.split(" ")
        if "cancel" in words or "council" in words:
            return
        for word in words:
            if word == "exit" or word == "quit":
                self.running = False
                self.state = "Stopped"
                self.active = False
            elif word == "give" or word == "get":
                self.active = True
                self.state = "Searching"

                point = words.index(word) + 1
                queryList = words[point:]
                query = ""
                for i in queryList:
                    if i != "assistant":
                        query += f"{i} "
                if self.perms.exceptExternalAPICommands():
                    query = query.replace("assistant", "")
                    print(query)
                    results = api.search(q=query, apikey="d4d4cd92f4314e493fbcde0dbd0836a43ee1c9de7ddd02727a4e3429ca30ca05", location="London, England, United Kingdom")
                    closestPlace = results["local_results"]["places"][0]
                    print(f"{closestPlace["title"]} at {closestPlace["address"]}")
                else:
                    pass
            elif "enable" in word or "activate" in word:
                if "external" in text:
                    self.perms.ExternalAPIAccess = True
            elif "toggle" in word:
                self.perms.ExternalAPICommands = not self.perms.ExternalAPIAccess



    class Permissions:
        def __init__(self):
            self.ExternalAPIAccess = False

        def exceptExternalAPICommands(self):
            if not self.ExternalAPIAccess:
                print("External API is not available")
                return False
            else:
                return True