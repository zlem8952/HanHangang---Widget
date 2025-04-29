import requests
import tkinter as tk
import threading

class HangangWidget(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("한강 물 온도")
        self.geometry("320x85+30+30")
        self.resizable(False, False)
        self.is_pinned = True
        self.set_topmost(self.is_pinned)
        self.configure(bg="#23272e")
        self.overrideredirect(True)

        # 캔버스
        self.canvas = tk.Canvas(self, width=320, height=85, bg="#23272e", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_rectangle(5, 5, 315, 80, outline="#2c313c", width=2, fill="#23272e")

        # 온도 표시 (글자 크기 줄임)
        self.label = tk.Label(self, text="한강 수온: 불러오는 중...", 
                             font=("맑은 고딕", 13, "bold"), fg="#61dafb", bg="#23272e")
        self.label.place(relx=0.5, rely=0.5, anchor="center")

        # 핀 & 닫기 버튼 (이모지)
        self.add_control_buttons()
        self.attributes("-alpha", 0.93)
        self.after(100, self.update_temperature)  # 프로그램 시작 후 곧바로 갱신 시작
        self.bind("<ButtonPress-1>", self.start_move)
        self.bind("<B1-Motion>", self.do_move)

    def add_control_buttons(self):
        self.pin_button = tk.Button(self, text="📌", command=self.toggle_pin,
                                   font=("맑은 고딕", 12), bd=0, bg="#23272e", 
                                   activebackground="#2c313c", cursor="hand2")
        self.pin_button.place(x=270, y=10, width=30, height=30)

        self.close_button = tk.Button(self, text="×", command=self.destroy,
                                     font=("맑은 고딕", 16), bd=0, bg="#23272e", 
                                     activebackground="#2c313c", cursor="hand2")
        self.close_button.place(x=290, y=10, width=30, height=30)

    def set_topmost(self, state):
        self.attributes("-topmost", 1 if state else 0)

    def toggle_pin(self):
        self.is_pinned = not self.is_pinned
        self.set_topmost(self.is_pinned)
        self.pin_button.config(text="📌" if self.is_pinned else "📍")

    def start_move(self, event):
        self._x = event.x
        self._y = event.y

    def do_move(self, event):
        x = self.winfo_x() + event.x - self._x
        y = self.winfo_y() + event.y - self._y
        self.geometry(f"+{x}+{y}")

    def update_temperature(self):
        def fetch_data():
            try:
                res = requests.get("https://api.ivl.is/hangangtemp", timeout=5)
                data = res.json()
                if data.get("success") and "temperature" in data and "time" in data:
                    temp = data["temperature"]
                    time = data["time"]
                    self.label.config(text=f"수온: {temp}°C   시간: {time}")
                else:
                    self.label.config(text="정보 없음")
            except Exception as e:
                self.label.config(text="정보 없음")
            finally:
                # 반드시 메인스레드에서 반복 예약!
                self.after(600000, self.update_temperature)
        threading.Thread(target=fetch_data, daemon=True).start()

if __name__ == "__main__":
    app = HangangWidget()
    app.mainloop()
