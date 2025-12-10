# -*- coding: utf-8 -*-
"""
Sincroniza generated_posts para docs/posts (GitHub Pages)
"""

import shutil
import json
from pathlib import Path

print("\n" + "="*80)
print("SINCRONIZAÇÃO: generated_posts → docs/posts")
print("="*80)

# Diretórios
source_dir = Path("generated_posts")
docs_posts_dir = Path("docs/posts")

# 1. Copiar index.json
print("\n1. Copiando index.json...")
source_index = source_dir / "index.json"
dest_index = docs_posts_dir / "index.json"

if source_index.exists():
    shutil.copy2(source_index, dest_index)
    print(f"   ✅ Copiado: {source_index} → {dest_index}")
    
    # Mostrar quantos posts
    with open(source_index, 'r', encoding='utf-8') as f:
        data = json.load(f)
        posts_count = len(data.get('posts', []))
        print(f"   📊 Total de posts: {posts_count}")
else:
    print(f"   ❌ Arquivo não encontrado: {source_index}")

# 2. Sincronizar estrutura de pastas (symlink ou cópia)
print("\n2. Criando estrutura de pastas...")

# GitHub Pages precisa que docs/ tenha acesso aos posts
# Opção: criar symlink ou copiar tudo

# Verificar se já existe link simbólico
generated_link = Path("docs/generated_posts")

if not generated_link.exists():
    print(f"   Criando link simbólico: docs/generated_posts → generated_posts/")
    try:
        # Windows: criar junction (funciona sem admin)
        import subprocess
        subprocess.run(['mklink', '/J', str(generated_link.absolute()), str(source_dir.absolute())], shell=True, check=True)
        print(f"   ✅ Link criado com sucesso")
    except Exception as e:
        print(f"   ⚠️ Não foi possível criar link: {e}")
        print(f"   💡 Alternativa: Copiar arquivos manualmente ou ajustar paths no viewer")
else:
    print(f"   ℹ️  Link já existe: {generated_link}")

print("\n" + "="*80)
print("SINCRONIZAÇÃO CONCLUÍDA!")
print("="*80)
print("\n📌 Próximos passos:")
print("1. git add docs/")
print("2. git commit -m 'Update GitHub Pages viewer'")
print("3. git push")
print("\nO GitHub Pages será atualizado em ~1-2 minutos")
print("="*80 + "\n")
