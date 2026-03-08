import cv2
import time

class Registration:
    def __init__(self, user_email, user_password, user_name):
        self.user_email = user_email
        self.user_password = user_password
        self.user_name = user_name
        self.check_email_first = "@gmail.com"
        self.check_email_second = "@icloud.com"
        self.allowed_end = "&$@#"   

    def result(self):
        if not (self.check_email_first in self.user_email or self.check_email_second in self.user_email):
            print("Неверный email (нужен @gmail.com или @icloud.com)")
            return
        if not self.user_password or not self.user_password[0].isupper():
            print("Пароль должен начинаться с заглавной буквы")
            return
        if self.user_password[-1] not in self.allowed_end:
            print("Пароль должен заканчиваться на один из символов: & $ @ #")
            return
        time.sleep(2)
        print("Пройдите видеопроверку! (10 сек)")
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Не удалось открыть камеру")
            return
        start = time.time()
        passed = False

        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    print("Не удалось получить кадр с камеры")
                    break
                cv2.imshow("Camera", frame)
                if time.time() - start >= 10:
                    passed = True
                    break
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    print("Вы вышли из проверки")
                    break
        finally:
            cap.release()
            cv2.destroyAllWindows()

        if passed:
            print(f"Вы успешно прошли видеопроверку, {self.user_name}! ✅")
        else:
            print("Видеопроверка не пройдена ❌")
            
user_email = input("ПОЧТА: ")
user_name = input("ВАША ИМЯ: ")
user_password = input("СОЗДАЙТЕ ПАРОЛЬ: ")
cl = Registration(user_email, user_password, user_name)
cl.result()

    

