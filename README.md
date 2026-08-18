# DexForge 🔴

> 🚧 **Projeto em construção.** Acompanhe o progresso pelas fases abaixo.

Uma Pokédex completa, construída como projeto de portfólio full stack — busca, coleção pessoal, comparador, team builder e muito mais.

## Stack

**Frontend:** Next.js · TypeScript · Tailwind CSS · shadcn/ui · TanStack Query

**Backend:** FastAPI · SQLAlchemy · PostgreSQL · Redis · JWT + OAuth Google

**Infra:** Docker · GitHub Actions · Vercel · Railway · Neon · Upstash

## Status do desenvolvimento

- [ ] Fase 1 — Base e Autenticação
- [ ] Fase 2 — Busca e Detalhes
- [ ] Fase 3 — Favoritos e Coleção
- [ ] Fase 4 — Comparador e Team Builder
- [ ] Fase 5 — Dashboard, Conquistas e Deploy

## Como rodar localmente

```bash
# Clonar o repositório
git clone https://github.com/SEU_USUARIO/dexforge.git
cd dexforge

# Copiar os arquivos de variáveis de ambiente
cp frontend/.env.example frontend/.env.local
cp backend/.env.example backend/.env

# Subir com Docker
docker compose up
```

## Licença

Este projeto está sob a licença MIT — veja [LICENSE](./LICENSE) para detalhes.
