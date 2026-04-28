from database import Database
from app import App

if __name__ == "__main__":
    db = Database()
    app = App(db)
    app.mainloop()