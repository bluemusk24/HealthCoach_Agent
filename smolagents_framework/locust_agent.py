from locust import HttpUser, between, task

class HealthCoachUser(HttpUser):       
    wait_time = between(1,2)                    

    @task
    def send_request(self):
        self.client.post("/", json={
            "goal": "Build Muscle",
            "dietary_preference": "Vegan"
        })