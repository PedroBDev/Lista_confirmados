from app import create_app, db

app = create_app()

# Garante que o contexto da aplicação está ativo
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)
