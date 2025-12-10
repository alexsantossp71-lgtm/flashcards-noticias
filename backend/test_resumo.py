"""
Teste para verificar que o resumo não contém placeholders
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.ollama_service import OllamaService

def test_summary_generation():
    print("="*70)
    print("🧪 TESTE DE GERAÇÃO DE RESUMO")
    print("="*70)
    
    service = OllamaService()
    
    # Testar se Ollama está disponível
    if not service.check_health():
        print("\n⚠️  Ollama não está rodando. Inicie o Ollama primeiro.")
        return
    
    print("\n✅ Ollama está rodando")
    print("\n📝 Testando geração de conteúdo...")
    print("-" * 70)
    
    try:
        result = service.generate_flashcard_content(
            headline="Brasil aprova nova lei sobre IA",
            url="https://exemplo.com/noticia",
            style_prompt="photorealistic",
            source="G1",
            article_text="O Congresso Nacional aprovou hoje uma nova legislação sobre inteligência artificial. A lei estabelece diretrizes para o uso ético de IA no país."
        )
        
        summary = result.get('tiktokSummary', '')
        
        print("\n📄 RESUMO GERADO:")
        print("-" * 70)
        print(summary)
        print("-" * 70)
        
        # Verificar se contém placeholders indesejados
        placeholders = ["Parágrafo 1", "Parágrafo 2", "[contexto", "[detalhes"]
        
        found_placeholders = []
        for placeholder in placeholders:
            if placeholder.lower() in summary.lower():
                found_placeholders.append(placeholder)
        
        if found_placeholders:
            print(f"\n❌ ERRO: Resumo contém placeholders: {', '.join(found_placeholders)}")
            print("   O prompt precisa ser ajustado!")
            return False
        else:
            print("\n✅ SUCESSO: Resumo não contém placeholders!")
            print("   O conteúdo foi gerado naturalmente.")
            return True
            
    except Exception as e:
        print(f"\n❌ Erro ao gerar conteúdo: {e}")
        return False

if __name__ == "__main__":
    test_summary_generation()
