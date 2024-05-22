from flask import Flask, render_template_string, request

app = Flask(__name__)

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Catálogo de Productos</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f9;
            margin: 0;
            padding: 20px;
        }
        h1 {
            color: #333;
        }
        form {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin: 10px 0 5px;
        }
        input[type="text"] {
            width: calc(100% - 22px);
            padding: 10px;
            margin-bottom: 10px;
        }
        button {
            background-color: #5c67f2;
            color: white;
            border: none;
            padding: 10px 20px;
            cursor: pointer;
            border-radius: 5px;
            font-size: 16px;
        }
        button:hover {
            background-color: #4a54e1;
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        table, th, td {
            border: 1px solid #ddd;
        }
        th, td {
            text-align: left;
            padding: 8px;
        }
        th {
            background-color: #f2f2f2;
        }
        p {
            color: #ff0000;
        }
    </style>
</head>
<body>
    <h1>Catálogo de productos</h1>
    <form method="POST">
        <label for="itemName">Nombre del artículo:</label>
        <input type="text" id="itemName" name="itemName" required>
        <label for="itemPrice">Precio del artículo:</label>
        <input type="text" id="itemPrice" name="itemPrice" pattern="[0-9]+(\.[0-9]{1,2})?" required>
        <button type="submit">Registrar artículo</button>
    </form>

    {% if errorMessage %}
        <p>{{ errorMessage }}</p>
    {% endif %}

    {% if itemList %}
        <h2>Inventario de productos</h2>
        <table>
            <tr>
                <th>Artículo</th>
                <th>Precio</th>
                <th>IVA</th>
                <th>Total con IVA</th>
            </tr>
            {% for item in itemList %}
                <tr>
                    <td>{{ item.articleName }}</td>
                    <td>{{ item.articlePrice }}</td>
                    <td>{{ item.articleIVA }}</td>
                    <td>{{ item.totalPriceWithIVA }}</td>
                </tr>
            {% endfor %}
        </table>
    {% endif %}
</body>
</html>
"""

itemList = []

@app.route('/', methods=['GET', 'POST'])
def home():
    global itemList
    errorMessage = None
    if request.method == 'POST':
        articleName = request.form.get('itemName').strip()
        articlePriceStr = request.form.get('itemPrice').strip()

        try:
            articlePrice = float(articlePriceStr)

            if not articleName.replace(" ", "").isalpha():
                errorMessage = "El nombre del artículo debe contener solo letras y espacios."
            elif articlePrice < 0:
                errorMessage = "El precio debe ser un valor positivo."
            else:
                articleIVA = articlePrice * 0.16  # Suponiendo un IVA del 16%
                totalPriceWithIVA = articlePrice + articleIVA

                item = {
                    'articleName': articleName,
                    'articlePrice': articlePrice,
                    'articleIVA': articleIVA,
                    'totalPriceWithIVA': totalPriceWithIVA
                }
                itemList.append(item)
        except ValueError:
            errorMessage = "Asegúrese de que el precio introducido es un número válido."

    return render_template_string(html_template, itemList=itemList, errorMessage=errorMessage)

if __name__ == '__main__':
    app.run(debug=True)

