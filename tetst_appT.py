from app import app

client = app.test_client()

def submit_form(val1, val2, action):
    return client.post(
        "/",
        data={"val1": str(val1), "val2": str(val2), "action": action}
    )

def test_homepage():
    response = client.get("/")
    assert response.status_code == 200
    assert "Menu-Driven Application" in response.get_data(as_text=True)

def test_option1():
    response = submit_form(10, 5, "opt1")
    assert response.status_code == 200
    assert "15.0" in response.get_data(as_text=True)

def test_option2():
    response = submit_form(10, 5, "opt2")
    assert response.status_code == 200
    assert "5.0" in response.get_data(as_text=True)

def test_invalid_input():
    response = client.post("/", data={"val1": "abc", "action": "opt1"})
    assert response.status_code == 200
    assert "Invalid input" in response.get_data(as_text=True)