from locust import HttpUser, TaskSet, task, between, events
import random
import shutil
import os

# Fichiers à sauvegarder et restaurer
JSON_FILES = ["clubs.json", "competitions.json"]

# Sauvegarde des fichiers JSON avant le début des tests
@events.test_start.add_listener
def on_test_start(**kwargs):
    for file in JSON_FILES:
        if os.path.exists(file):
            shutil.copy2(file, f"{file}.backup")

# Restauration des fichiers JSON à la fin des tests
@events.test_stop.add_listener
def on_test_stop(**kwargs):
    for file in JSON_FILES:
        backup_file = f"{file}.backup"
        if os.path.exists(backup_file):
            shutil.copy2(backup_file, file)
            os.remove(backup_file)

class UserBehavior(TaskSet):
    def on_start(self):
        # Clubs et compétitions pour les tests
        self.clubs = ["Simply Lift", "Iron Temple", "She Lifts"]
        self.competitions = ["Spring Festival", "Fall Classic", "Winter Showdown"]
        
    @task
    def view_competitions(self):
        # Consulter la liste des compétitions
        with self.client.get("/competitions", catch_response=True) as response:
            if response.elapsed.total_seconds() > 5:
                response.failure("Loading competitions took more than 5 seconds")
            else:
                response.success()

    @task
    def view_points(self):
        # Consulter le tableau des points
        with self.client.get("/points", catch_response=True) as response:
            if response.elapsed.total_seconds() > 2:
                response.failure("Loading points took more than 2 seconds")
            else:
                response.success()
                
    @task
    def purchase_places(self):
        # Acheter des places
        club = random.choice(self.clubs)
        competition = random.choice(self.competitions)
        places = random.randint(1, 5)
        
        data = {
            "club": club,
            "competition": competition,
            "places": places
        }
        
        with self.client.post("/purchasePlaces", data=data, catch_response=True) as response:
            if response.elapsed.total_seconds() > 2:
                response.failure("Purchase places took more than 2 seconds")
            else:
                response.success()
    
    @task
    def test_points_update(self):
        """Test complet vérifiant le temps de mise à jour des points"""
        # 1. Consulter les points avant l'achat
        with self.client.get("/points", catch_response=True) as response:
            if response.elapsed.total_seconds() > 2:
                response.failure("Initial points load took more than 2 seconds")
            else:
                response.success()
        
        # 2. Acheter des places
        club = random.choice(self.clubs)
        competition = random.choice(self.competitions)
        places = random.randint(1, 3)
        
        data = {
            "club": club,
            "competition": competition,
            "places": places
        }
        
        with self.client.post("/purchasePlaces", data=data, catch_response=True) as response:
            purchase_response_time = response.elapsed.total_seconds()
            response.success()
        
        # 3. Vérifier les points mis à jour
        start_time = response.elapsed.total_seconds()
        with self.client.get("/points", catch_response=True) as response:
            points_update_time = response.elapsed.total_seconds()
            total_update_time = purchase_response_time + points_update_time
            
            if total_update_time > 2:
                response.failure(f"Total points update time took {total_update_time:.2f} seconds, exceeding 2 seconds limit")
            else:
                response.success()

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 3)
    host = "http://127.0.0.1:5000"