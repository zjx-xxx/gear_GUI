# tabs/tab_settings.py
import customtkinter as ctk

TAB_LABEL = "设置"

class Settings:
    def __init__(self, tabview):
        self.frame = ctk.CTkFrame(tabview.tab(TAB_LABEL))

        ctk.CTkLabel(self.frame, text="程序设置", font=ctk.CTkFont(size=16)).pack(pady=20)

        self.theme_option = ctk.CTkOptionMenu(self.frame, values=["Light", "Dark", "System"], command=self.change_theme)
        self.theme_option.pack(pady=10)
        self.theme_option.set("Dark")

        self.scale_option = ctk.CTkOptionMenu(self.frame, values=["80%", "100%", "120%"], command=self.change_scaling)
        self.scale_option.pack(pady=10)
        self.scale_option.set("100%")

    def change_theme(self, mode):
        ctk.set_appearance_mode(mode)

    def change_scaling(self, scale):
        factor = int(scale.replace("%", "")) / 100
        ctk.set_widget_scaling(factor)
