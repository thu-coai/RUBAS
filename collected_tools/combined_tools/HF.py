from BaseEnv import BaseEnv

class HF(BaseEnv):
    def __init__(self, *, parameters=None):
        super().__init__()
        self.parameters = parameters if parameters is not None else {}
        self.files = self.parameters.get("files", {})
        self.websites = self.parameters.get("websites", {})
        self.databases = self.parameters.get("databases", {})
        self.hosts = self.parameters.get("hosts", {})
        self.quotes = {
            "en": ["To be or not to be.", "The only thing we have to fear is fear itself."],
            "es": ["La vida es sueño.", "El que no arriesga no gana."],
        }
        self.jokes = [
            "Why did the computer get cold? Because it left its Windows open.",
            "Why don't programmers like nature? It has too many bugs.",
        ]
        self.payloads = ["payload1", "payload2", "payload3"]
        self.urls = ["http://example.com/1", "http://example.com/2"]
        self.books = [
            {"id": "1", "title": "Book One", "author": "Author A", "language": "en"},
            {"id": "2", "title": "Book Two", "author": "Author B", "language": "fr"},
        ]
        self.poetry_db = [
            {"author": "Emily Dickinson", "title": "Hope", "lines": ["Hope is the thing with feathers"], "linecount": 1},
            {"author": "Robert Frost", "title": "Fire and Ice", "lines": ["Some say the world will end in fire"], "linecount": 1},
        ]
        self.rent_estimates = [
            {"address": "123 Main St", "estimate": 1200},
            {"address": "456 Elm St", "estimate": 1500},
        ]
        self.company_db = [
            {"company": "Acme Corp", "address": "1 Acme Way"},
            {"company": "Acme Corporation", "address": "1 Acme Way"},
        ]

    def read_file(self, *, file_path):
        content = self.files.get(file_path)
        if content is not None:
            return {"success": True, "data": {"content": content}}
        else:
            return {"success": False, "message": "File not found."}

    def retrieve_website(self, *, website):
        result = self.websites.get(website)
        if result is not None:
            return {"success": True, "data": {"website": website, "result": result}}
        else:
            return {"success": False, "message": "Website not found."}

    def select_database_data(self, *, query):
        # Simulate by returning a mock result for any query
        return {"success": True, "data": {"query": query, "result": "Simulated database result."}}

    def generate_string(self, *, len, cnt):
        try:
            length = int(len)
            count = int(cnt)
        except Exception:
            return {"success": False, "message": "Parameters 'len' and 'cnt' must be integers."}
        import random
        import string
        strings = []
        for _ in range(count):
            s = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
            strings.append(s)
        return {"success": True, "data": {"strings": strings}}

    def blacklist_ip(self, *, limit):
        try:
            lim = int(limit)
        except Exception:
            return {"success": False, "message": "Parameter 'limit' must be an integer."}
        return {"success": True, "data": {"urls": self.urls[:lim]}}

    def query_payloads(self, *, limit):
        try:
            lim = int(limit)
        except Exception:
            return {"success": False, "message": "Parameter 'limit' must be an integer."}
        return {"success": True, "data": {"payloads": self.payloads[:lim]}}

    def company_name_match(self, *, function, process, category, source, connection, table, column, json, html):
        # Simulate matching by returning similar company names
        matches = []
        for i in range(len(self.company_db)):
            for j in range(i+1, len(self.company_db)):
                if self.company_db[i]["company"].lower().replace("corp", "").strip() == self.company_db[j]["company"].lower().replace("corporation", "").strip():
                    matches.append((self.company_db[i]["company"], self.company_db[j]["company"]))
        return {"success": True, "data": {"matches": matches, "format": "json" if json == "true" else "html" if html == "true" else "text"}}

    def get_host_history(self, *, host_name):
        history = self.hosts.get(host_name, [])
        return {"success": True, "data": {"host_name": host_name, "history": history}}

    def get_random_number(self, *, min, max, cnt):
        try:
            min_val = int(min)
            max_val = int(max)
            count = int(cnt)
        except Exception:
            return {"success": False, "message": "Parameters 'min', 'max', and 'cnt' must be integers."}
        import random
        numbers = [random.randint(min_val, max_val) for _ in range(count)]
        return {"success": True, "data": {"numbers": numbers}}

    def gutendex(self, *, author_year_start, author_year_end, copyright, ids, languages, mime_type, search, sort, topic, id):
        # Simulate by filtering books by language and id
        filtered = self.books
        if languages:
            langs = [l.strip() for l in languages.split(",")]
            filtered = [b for b in filtered if b.get("language") in langs]
        if id:
            filtered = [b for b in filtered if b.get("id") == id]
        return {"success": True, "data": {"books": filtered}}

    def paper_rank(self, *, domains):
        # Simulate by returning a mock rank for each domain
        doms = [d.strip() for d in domains.split(",")]
        ranks = {d: 100 - i*10 for i, d in enumerate(doms)}
        return {"success": True, "data": {"ranks": ranks}}

    def poetry(self, *, input_field, search_term, search_type, output_field, form):
        # Simulate by searching poetry_db
        results = []
        for entry in self.poetry_db:
            if input_field in entry and ((search_type == "abs" and str(entry[input_field]) == search_term) or (search_type != "abs" and search_term in str(entry[input_field]))):
                result = {field: entry.get(field) for field in output_field.split(",") if field in entry}
                results.append(result)
        return {"success": True, "data": {"results": results, "format": form}}

    def query_database(self, *, table_name, column_names, condition):
        # Simulate by returning a mock result
        return {"success": True, "data": {"table": table_name, "columns": column_names.split(","), "condition": condition, "result": "Simulated database query result."}}

    def query_host(self, *, host):
        info = self.hosts.get(host, {"info": "No info available."})
        return {"success": True, "data": {"host": host, "info": info}}

    def query_url(self, *, q_url):
        if q_url in self.urls:
            return {"success": True, "data": {"url": q_url, "info": "URL found in database."}}
        else:
            return {"success": False, "message": "URL not found."}

    def random_cold_jokes(self):
        import random
        joke = random.choice(self.jokes)
        return {"success": True, "data": {"joke": joke}}

    def random_quote(self, *, lang_code):
        quotes = self.quotes.get(lang_code, self.quotes.get("en", []))
        import random
        quote = random.choice(quotes) if quotes else "No quote available."
        return {"success": True, "data": {"quote": quote}}

    def rent_estimate(self, *, address, latitude, longitude, property_type, bedrooms, bathrooms, square_footage, max_radius, days_old, comp_count):
        # Simulate by returning a mock estimate
        for entry in self.rent_estimates:
            if entry["address"] == address:
                return {"success": True, "data": {"address": address, "estimate": entry["estimate"]}}
        return {"success": True, "data": {"address": address, "estimate": 1000}}