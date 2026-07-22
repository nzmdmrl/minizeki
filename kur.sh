#!/usr/bin/env bash
# Minizeki tek komut kurulum
set -e

echo "=========================================="
echo "  MINIZEKI KURULUM"
echo "=========================================="

# Backend
echo ""
echo "[1/3] Backend bagimliliklar..."
cd backend
python3 -m venv venv 2>/dev/null || true
source venv/bin/activate
pip install -q -r requirements.txt

echo "[2/3] Veritabani + soru bankasi..."
python content/seed.py

deactivate
cd ..

# Frontend
echo ""
echo "[3/3] Frontend bagimliliklar..."
cd frontend
npm install --silent
echo "NEXT_PUBLIC_API_URL=http://localhost:8420" > .env.local
cd ..

echo ""
echo "=========================================="
echo "  KURULUM TAMAM"
echo "=========================================="
echo ""
echo "  Baslatmak icin 2 terminal acin:"
echo ""
echo "  Terminal 1 (backend, port 8420):"
echo "    cd backend && source venv/bin/activate && python main.py"
echo ""
echo "  Terminal 2 (frontend, port 3420):"
echo "    cd frontend && npm run dev"
echo ""
echo "  Sonra: http://localhost:3420"
echo ""
echo "  ---"
echo "  ADMIN PANELI (istege bagli):"
echo "    1. Once siteden kayit olun"
echo "    2. cd backend && source venv/bin/activate"
echo "       python content/make_admin.py sizin@epostaniz.com"
echo "    3. Sunucuyu admin sifresiyle baslatin:"
echo "       ADMIN_PASSWORD='guclu-bir-sifre' python main.py"
echo "    4. http://localhost:3420/admin"
echo ""
