from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'secret_key'

# Гача магадлалууд
rarity_rates = {"N": 33, "N+": 25, "R": 20, "R+": 15, "SR": 5, "SR+": 2}

# Зургийн замууд
#image
rarity_images = {
    "N": [
        "images/N_card1.jpg", "images/N_card2.jpg", "images/N_card3.jpg",
        "images/N_card4.jpg", "images/N_card5.jpg", "images/N_card6.jpg",
        "images/N_card7.jpg", "images/N_card8.jpg", "images/N_card9.jpg",
        "images/N_card10.jpg", "images/N_card11.jpg", "images/N_card12.jpg",
        "images/N_card13.jpg", "images/N_card14.jpg", "images/N_card15.jpg",
        "images/N_card16.jpg", "images/N_card17.jpg", "images/N_card18.jpg",
        "images/N_card19.jpg", "images/N_card20.jpg", "images/N_card21.jpg",
        "images/N_card22.jpg", "images/N_card23.jpg", "images/N_card24.jpg",
        "images/N_card25.jpg", "images/N_card26.jpg", "images/N_card27.jpg",
        "images/N_card28.jpg", "images/N_card29.jpg", "images/N_card30.jpg",
        "images/N_card31.jpg", "images/N_card32.jpg", "images/N_card33.jpg"
    ],
    "N+": [
        "images/N+_card1.jpg", "images/N+_card2.jpg", "images/N+_card3.jpg",
        "images/N+_card4.jpg", "images/N+_card5.jpg", "images/N+_card6.jpg",
        "images/N+_card7.jpg", "images/N+_card8.jpg", "images/N+_card9.jpg",
        "images/N+_card10.jpg", "images/N+_card11.jpg", "images/N+_card12.jpg",
        "images/N+_card13.jpg", "images/N+_card14.jpg", "images/N+_card15.jpg",
        "images/N+_card16.jpg", "images/N+_card17.jpg", "images/N+_card18.jpg",
        "images/N+_card19.jpg", "images/N+_card20.jpg", "images/N+_card21.jpg",
        "images/N+_card22.jpg", "images/N+_card23.jpg", "images/N+_card24.jpg",
        "images/N+_card25.jpg"
    ],
    "R": [
        "images/R_card1.jpg", "images/R_card2.jpg", "images/R_card3.jpg",
        "images/R_card4.jpg", "images/R_card5.jpg", "images/R_card6.jpg",
        "images/R_card7.jpg", "images/R_card8.jpg", "images/R_card9.jpg",
        "images/R_card10.jpg", "images/R_card11.jpg", "images/R_card12.jpg",
        "images/R_card13.jpg", "images/R_card14.jpg", "images/R_card15.jpg",
        "images/R_card16.jpg", "images/R_card17.jpg", "images/R_card18.jpg",
        "images/R_card19.jpg", "images/R_card20.jpg"
    ],
    "R+": [
        "images/R+_card1.jpg", "images/R+_card2.jpg", "images/R+_card3.jpg",
        "images/R+_card4.jpg", "images/R+_card5.jpg", "images/R+_card6.jpg",
        "images/R+_card7.jpg", "images/R+_card8.jpg", "images/R+_card9.jpg",
        "images/R+_card10.jpg", "images/R+_card11.jpg", "images/R+_card12.jpg",
        "images/R+_card13.jpg", "images/R+_card14.jpg", "images/R+_card15.jpg"
    ],
    "SR": [
        "images/SR_card1.jpg", "images/SR_card2.jpg", "images/SR_card3.jpg",
        "images/SR_card4.jpg", "images/SR_card5.jpg"
    ],
    "SR+": ["images/SR+_card1.jpg", "images/SR+_card2.jpg"]
}


# Шинэчилсэн draw_gacha функц
def draw_gacha(single=True):
    if single:
        rarity = random.choices(list(rarity_rates.keys()),
                                weights=rarity_rates.values(),
                                k=1)[0]
        image = random.choice(rarity_images[rarity])
        return {"rarity": rarity, "image": image}
    else:
        results = []
        for _ in range(10):
            rarity = random.choices(list(rarity_rates.keys()),
                                    weights=rarity_rates.values(),
                                    k=1)[0]
            image = random.choice(rarity_images[rarity])
            results.append({"rarity": rarity, "image": image})
        # 11連ガチャ сүүлийн карт SR
        results.append({
            "rarity": "SR",
            "image": random.choice(rarity_images["SR"])
        })
        return results


@app.route('/')
def index():
    session.setdefault('results', [])
    return render_template('index.html', results=session['results'])


@app.route('/gacha', methods=['POST'])
def gacha():
    if 'single' in request.form:
        result = draw_gacha()
        session['results'].append(result)
    elif 'multi' in request.form:
        result = draw_gacha(single=False)
        session['results'].extend(result)
    session.modified = True
    return redirect(url_for('index'))


@app.route('/reset')
def reset():
    session['results'] = []
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0')