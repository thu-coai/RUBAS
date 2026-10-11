from BaseEnv import BaseEnv

class CatEye(BaseEnv):
    def __init__(self, *, parameters=None):
        super().__init__()
        self.parameters = parameters if parameters is not None else {}
        self.movies = self.parameters.get("movies", [
            {
                "id": "m1",
                "name": "The Cat Returns",
                "director": "Hiroyuki Morita",
                "actors": ["Chizuru Ikewaki", "Yoshihiko Hakamada"],
                "genre": "Animation",
                "release_date": "2002-07-20"
            },
            {
                "id": "m2",
                "name": "Cat's Eye",
                "director": "Yoshio Takeuchi",
                "actors": ["Chika Sakamoto", "Keiko Toda"],
                "genre": "Action",
                "release_date": "1988-03-19"
            }
        ])
        self.showtimes = self.parameters.get("showtimes", [
            {
                "id": "s1",
                "movie_id": "m1",
                "theater_location": "Downtown Cinema",
                "time": "2024-07-01 19:00",
                "available_seats": ["A1", "A2", "A3"]
            },
            {
                "id": "s2",
                "movie_id": "m2",
                "theater_location": "City Mall",
                "time": "2024-07-01 20:00",
                "available_seats": ["B1", "B2"]
            }
        ])
        self.tickets = self.parameters.get("tickets", [])
        self.comments = self.parameters.get("comments", [])
        self.viewing_history = self.parameters.get("viewing_history", {})
        self.reminders = self.parameters.get("reminders", [])
        self.user_comments = self.parameters.get("user_comments", {})

    def search_movie(self, *, movie_name, genre=None, release_date=None):
        results = []
        for movie in self.movies:
            if movie_name.lower() in movie["name"].lower():
                if genre and genre.lower() != movie.get("genre", "").lower():
                    continue
                if release_date and release_date not in movie.get("release_date", ""):
                    continue
                results.append(movie)
        return {
            "success": True,
            "data": {"movies": results}
        }

    def view_showtimes(self, *, movie_id, theater_location=None):
        results = []
        for show in self.showtimes:
            if show["movie_id"] == movie_id:
                if theater_location and theater_location.lower() not in show["theater_location"].lower():
                    continue
                results.append(show)
        return {
            "success": True,
            "data": {"showtimes": results}
        }

    def place_ticket(self, *, movie_id, showtime_id, seats, payment_method):
        showtime = None
        for s in self.showtimes:
            if s["id"] == showtime_id and s["movie_id"] == movie_id:
                showtime = s
                break
        if not showtime:
            return {"success": False, "message": "Showtime not found."}
        unavailable = [seat for seat in seats if seat not in showtime["available_seats"]]
        if unavailable:
            return {"success": False, "message": f"Seats not available: {unavailable}"}
        for seat in seats:
            showtime["available_seats"].remove(seat)
        ticket_id = f"t{len(self.tickets)+1}"
        ticket = {
            "id": ticket_id,
            "movie_id": movie_id,
            "showtime_id": showtime_id,
            "seats": seats,
            "payment_method": payment_method,
            "status": "pending"
        }
        self.tickets.append(ticket)
        return {"success": True, "data": {"ticket_id": ticket_id}}

    def pay_ticket(self, *, ticket_id, payment_method, payment_amount):
        ticket = None
        for t in self.tickets:
            if t["id"] == ticket_id:
                ticket = t
                break
        if not ticket:
            return {"success": False, "message": "Ticket not found."}
        ticket["status"] = "paid"
        ticket["payment_method"] = payment_method
        ticket["payment_amount"] = payment_amount
        return {"success": True, "message": "Payment successful."}

    def refund_ticket(self, *, ticket_id, refund_reason=None):
        ticket = None
        for t in self.tickets:
            if t["id"] == ticket_id:
                ticket = t
                break
        if not ticket:
            return {"success": False, "message": "Ticket not found."}
        ticket["status"] = "refunded"
        ticket["refund_reason"] = refund_reason
        return {"success": True, "message": "Refund processed."}

    def post_comment(self, *, movie_id, comment_text):
        comment = {
            "movie_id": movie_id,
            "comment_text": comment_text
        }
        self.comments.append(comment)
        return {"success": True, "message": "Comment posted."}

    def view_viewing_history(self, *, user_id):
        history = self.viewing_history.get(user_id, [])
        return {"success": True, "data": {"history": history}}

    def set_movie_reminder(self, *, movie_id, reminder_time):
        reminder = {
            "movie_id": movie_id,
            "reminder_time": reminder_time
        }
        self.reminders.append(reminder)
        return {"success": True, "message": "Reminder set."}

    def view_user_comment_history(self, *, user_id):
        comments = self.user_comments.get(user_id, [])
        return {"success": True, "data": {"comments": comments}}