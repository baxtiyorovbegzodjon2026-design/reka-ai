from backend.agents.research_agent import research_agent
from backend.services.gemini_service import gemini_service
from backend.services.molecule_service import molecule_service
from backend.services.pubchem_service import pubchem_service

class DiscoveryAgent:
    async def discover(self, query: str) -> dict:
        # 1. So'rovni dinamik ravishda tahlil qilish (har qanday kasallik uchun O'ZBEK tilida)
        prompt_uz = f"Foydalanuvchi so'rovi: '{query}'. Ushbu kasallik yoki dori uchun chuqur biotexnologik tahlil o'tkaz va natijani O'ZBEK tilida ber."
        research = await research_agent.investigate(prompt_uz)
        
        # 2. Molekulalarni generatsiya qilish
        candidates = gemini_service.generate_molecules(research.get("analysis", {}))
        
        processed_candidates = []
        for cand in candidates:
            smiles = cand.get("smiles", "")
            if not smiles:
                continue
                
            is_valid = molecule_service.validate_smiles(smiles)
            if not is_valid:
                continue
                
            props = molecule_service.calculate_properties(smiles)
            lipinski = molecule_service.check_lipinski(props)
            molblock = molecule_service.get_3d_molblock(smiles)
            svg = molecule_service.smiles_to_svg(smiles)
            
            # 3. O'zbekcha va Inglizcha Patent loyihasini yaratish
            patent_data = {
                "disease_query": query,
                "smiles": smiles,
                "rationale": cand.get("rationale", ""),
                "properties": props,
                "language": "uzbek_and_english" # Avtomatik ikki tilda chiqaradi
            }
            patent_draft = gemini_service.generate_patent_draft(patent_data)
            
            processed_candidates.append({
                "smiles": smiles,
                "rationale": cand.get("rationale", ""),
                "expected_affinity": cand.get("expected_affinity", "Unknown"),
                "properties": props,
                "lipinski": lipinski,
                "3d_molblock": molblock,
                "2d_svg": svg,
                "patent_draft": patent_draft
            })
            
        top_3 = processed_candidates[:3]
        
        return {
            "query": query,
            "research": research,
            "candidates": top_3
        }

discovery_agent = DiscoveryAgent()
