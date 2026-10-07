import json
import google.generativeai as genai
from backend.config import settings

genai.configure(api_key=settings.gemini_api_key)

class GeminiService:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-2.5-pro')

    def _clean_json(self, text: str) -> str:
        """JSON javobni tozalash uchun yordamchi funksiya"""
        text = text.strip()
        if text.startswith('```json'):
            text = text[7:]
        if text.startswith('```'):
            text = text[3:]
        if text.endswith('```'):
            text = text[:-3]
        return text.strip()

    def analyze_target(self, query: str) -> dict:
        prompt = f"""
        Foydalanuvchi so'rovi: "{query}"
        
        Siz Breka AI — professional dori vositalarini loyihalash sun'iy intellektisiz.
        Ushbu so'rov bo'yicha HAR QANDAY kasallik yoki dori maqsadini mukammal va chuqur tahlil qiling.
        Javob ma'lumotlarini O'ZBEK TILIDA bering.
        
        Quyidagi kalitlar bilan to'g'ri JSON obyektini qaytaring:
        - target_protein: string (biologik nishon oqsili nomi, masalan: "Alpha-synuclein" yoki "Beta-amyloid")
        - disease_mechanism: string (kasallik mexanizmi va patogenezi haqida batafsil o'zbekcha tushuntirish)
        - desired_properties: list of strings (molekuladan kutilayotgan farmakologik xossalar ro'yxati)
        - existing_drugs: list of strings (mavjud muqobil dorilar yoki davolash usullari)
        - novel_approach: string (Breka AI tomonidan taklif etilayotgan yangicha innovatsion yechim)
        
        Faqat va faqat to'g'ri JSON formatida javob bering.
        """
        response = self.model.generate_content(prompt)
        try:
            return json.loads(self._clean_json(response.text))
        except json.JSONDecodeError:
            return {"error": "JSON tahlilida xatolik yuz berdi."}

    def generate_molecules(self, analysis: dict) -> list[dict]:
        prompt = f"""
        Ushbu biotexnologik tahlil asosida: {json.dumps(analysis, ensure_ascii=False)}
        
        Ushbu nishon uchun 5 ta mutlaqo yangi, noyob va mos keluvchi nomzod SMILES strukturalarini generatsiya qiling.
        Tushuntirishlarni O'ZBEK TILIDA bering.
        
        Har bir obyekt uchun quyidagi kalitlarga ega JSON massivini qaytaring:
        - smiles: string (to'g'ri kimyoviy SMILES formulasi)
        - rationale: string (ushbu molekula nima uchun tanlangani va qanday ta'sir qilishi haqida o'zbekcha batafsil tushuntirish)
        - expected_affinity: string (kutilayotgan affinlik darajasi, masalan: "Yuqori (High)", "O'rta (Medium)")
        
        Faqat va faqat to'g'ri JSON formatida javob bering.
        """
        response = self.model.generate_content(prompt)
        try:
            return json.loads(self._clean_json(response.text))
        except json.JSONDecodeError:
            return []

    def generate_patent_draft(self, molecule_data: dict) -> dict:
        prompt = f"""
        Quyidagi nomzod molekula uchun rasmiy PATENT ARIZASI LOYIHASINI tayyorlang:
        {json.dumps(molecule_data, ensure_ascii=False)}
        
        Patent hujjatini O'ZBEK TILIDA (va xalqaro atamalari bilan) professional va mukammal shakllantiring.
        
        Quyidagi kalitlarga ega JSON obyektini qaytaring:
        - title: string (Patent sarlavhasi, masalan: "Neyrodegenerativ kasalliklarni davolash uchun yangi kichik molekulali birikmalar")
        - abstract: string (Ixtironing o'zbek tilidagi qisqacha mazmuni va afzalliklari)
        - claims: list of strings (Patent talablari va huquqiy bandlari ro'yxati)
        - background: string (Kasallik tarixi, dolzarbligi va mavjud muammolar)
        
        Faqat va faqat to'g'ri JSON formatida javob bering.
        """
        response = self.model.generate_content(prompt)
        try:
            return json.loads(self._clean_json(response.text))
        except json.JSONDecodeError:
            return {"error": "Patent JSON tahlilida xatolik yuz berdi."}

gemini_service = GeminiService()
