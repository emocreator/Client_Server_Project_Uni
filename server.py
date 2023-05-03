import socket
import threading
import random
previous_orders = {}

# dictionary of books and their details
books = {
    101: {"name": "More Peak District", "price": 12.99, "inventory": 10},
    102: {"name": "Lincolnshire Wolds", "price": 10.99, "inventory": 10},
    103: {"name": "Vale of York", "price": 11.99, "inventory": 10},
    104: {"name": "Peak District", "price": 12.99, "inventory": 10},
    105: {"name": "Snowdonia", "price": 13.99, "inventory": 10},
    106: {"name": "Malvern and Warwickshire", "price": 10.99, "inventory": 10},
    107: {"name": "Cheshire", "price": 12.99, "inventory": 10}
}
# dictionary of walks and their details
walks = [
    {"area": "PeakDistrict", "book": "More Peak District", "name": "Hathasage", "distance": 7, "difficulty": "Easy", "page": 67},
    {"area": "PeakDistrict", "book": "More Peak District", "name": "Hope and Win Hill", "distance": 4.5, "difficulty": "Medium", "page": 18},
    {"area": "Lincolnshire", "book": "Lincolnshire Wolds", "name": "Thornton Abbey", "distance": 3.5, "difficulty": "Easy", "page": 20},
    {"area": "Lincolnshire", "book": "Lincolnshire Wolds", "name": "Tennyson County", "distance": 5, "difficulty": "Hard", "page": 28},
    {"area": "York", "book": "Vale Of York", "name": "Cowlam and Cotham", "distance": 8, "difficulty": "Hard", "page": 64},
    {"area": "York", "book": "Vale of York", "name": "Fridaythorpe", "distance": 7, "difficulty": "Easy", "page": 42},
    {"area": "PeakDistrict", "book": "Peak District", "name": "Magpie Mine", "distance": 4.5, "difficulty": "Medium", "page": 20},
    {"area": "PeakDistrict", "book": "Peak District", "name": "Lord’s Seat", "distance": 5.5, "difficulty": "Easy", "page": 28},
    {"area": "NorthWales", "book": "Snowdonia", "name": "Around Aber", "distance": 4, "difficulty": "Hard", "page": 24},
    {"area": "NorthWales", "book": "Snowdonia", "name": "Yr Eifl", "distance": 3.5, "difficulty": "Medium", "page": 42},
    {"area": "Warwickshire", "book": "Malvern and Warwickshire", "name": "Edge Hill", "distance": 4, "difficulty": "Easy", "page": 28},
    {"area": "Warwickshire", "book": "Malvern and Warwickshire", "name": "Bidford-UponAvon", "distance": 8.5, "difficulty": "Medium", "page": 78},
    {"area": "Cheshire", "book": "Cheshire", "name": "Dane Valley", "distance": 8.5, "difficulty": "Easy", "page": 20},
    {"area": "Cheshire", "book": "Cheshire", "name": "Malpas", "distance": 8.5, "difficulty": "Medium", "page": 80},
    {"area": "Cheshire", "book": "Cheshire", "name": "Farndon", "distance": 8.5, "difficulty": "Hard", "page": 48},
    {"area": "Cheshire", "book": "Cheshire", "name": "Delamere Forest", "distance": 5.5, "difficulty": "Easy", "page": 30}]

orders = {}
def levenshtein_distance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        new_distances = [i2 + 1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                new_distances.append(distances[i1])
            else:
                new_distances.append(1 + min((distances[i1], distances[i1 + 1], new_distances[-1])))
        distances = new_distances
    return distances[-1]

def find_closest_match(word, word_list):
    distances = [levenshtein_distance(word, w) for w in word_list]
    closest_match_index = distances.index(min(distances))
    return word_list[closest_match_index]


def correct_typos(message):
    corrected_message = []
    areas = list(set([walk["area"] for walk in walks]))
    difficulties = list(set([walk["difficulty"] for walk in walks]))
    commands = ["Search", "Buy", "exit"]
    max_distance_threshold = 2
    
    for i, word in enumerate(message):
        if i == 0:  # Command
            closest_command = find_closest_match(word, commands)
            if levenshtein_distance(word, closest_command) <= max_distance_threshold:
                corrected_message.append(closest_command)
            else:
                corrected_message.append(word)
        elif i == 1 and message[0] == "Search":  # Area
            closest_area = find_closest_match(word, areas)
            if levenshtein_distance(word, closest_area) <= max_distance_threshold:
                corrected_message.append(closest_area)
            else:
                corrected_message.append(word)
        elif i == 4 and message[0] == "Search":  # Difficulty
            closest_difficulty = find_closest_match(word, difficulties)
            if levenshtein_distance(word, closest_difficulty) <= max_distance_threshold:
                corrected_message.append(closest_difficulty)
            else:
                corrected_message.append(word)
        else:
            corrected_message.append(word)
            
    return corrected_message

def handle_client(conn, addr):
    print("Connected by", addr)
    while True:
        data = conn.recv(1024).decode("utf-8")
        if not data:
            break
        message = data.strip().split(" ")
        message = correct_typos(message)
        
        print(message)
        try:
            if message[0] == "Search":
                area = message[1]
                min_distance = int(message[2])
                max_distance = int(message[3])
                difficulty = message[4]
                recommended_walks = []
                for walk in walks:
                    if walk["area"] == area and min_distance <= walk["distance"] <= max_distance and walk["difficulty"] == difficulty:
                        recommended_walks.append(f"{walk['name']}, {walk['book']}, pg {walk['page']}")
                if recommended_walks:
                    recommended_walks_str = "\n".join(recommended_walks)
                    conn.send(f"Recommended walks:\n{recommended_walks_str}".encode("utf-8"))
                else:
                    conn.send("No walks found for the given criteria".encode("utf-8"))

            elif message[0] == "Buy":
                customer_name = message[1]
                order = []
                order_cost = 0
                not_enough_books = []
                for i in range(2, len(message), 2):
                    book_number = int(message[i])
                    book_quantity = int(message[i + 1])
                    book = books.get(book_number)
                    if book:
                        if book["inventory"] >= book_quantity:
                            book_cost = book["price"] * book_quantity
                            order.append((book["name"], book_quantity, book_cost))
                            order_cost += book_cost
                            book["inventory"] -= book_quantity
                        else:
                            not_enough_books.append((book["name"], book["inventory"]))
                if not_enough_books:
                    not_enough_books_str = "\n".join([f"{book_name}: {inventory} available" for book_name, inventory in not_enough_books])
                    conn.send(f"Insufficient inventory for the following books:\n{not_enough_books_str}\n".encode("utf-8"))
                elif order:
                    if customer_name in orders:
                        previous_orders = orders[customer_name]
                        total_books = sum([order[1] for order in previous_orders + order])
                        if total_books > 50:
                            conn.send("Error: you have reached the maximum number of books you can buy".encode("utf-8"))
                        else:
                            order_cost_str = f"Order cost: £{order_cost:.2f}"
                            order_str = "\n".join([f"{book_name} x {book_quantity}: £{book_cost:.2f}" for book_name, book_quantity, book_cost in order])
                            if order_cost > 75:
                                order_cost_str += f"\nDiscount applied: £{order_cost * 0.1:.2f}"
                                order_cost -= order_cost * 0.1
                            conn.send(f"{order_str}\n{order_cost_str}".encode("utf-8"))
                            orders[customer_name] = previous_orders + order
                    else:
                        order_cost_str = f"Order cost: £{order_cost:.2f}"
                        order_str = "\n".join([f"{book_name} x {book_quantity}: £{book_cost:.2f}" for book_name, book_quantity, book_cost in order])
                        if order_cost > 75:
                            order_cost_str += f"\nDiscount applied: £{order_cost * 0.1:.2f}"
                            order_cost -= order_cost * 0.1
                        conn.send(f"{order_str}\n{order_cost_str}".encode("utf-8"))
                        orders[customer_name] = order
                else:
                    conn.send("No books ordered".encode("utf-8"))

            elif message[0] == "exit":
                break
            else:
                conn.send("Invalid request, Try a command in our command library".encode("utf-8"))
                
        except:
            conn.send("Didnt follow the write code criteria, its Search [Area Where Want to Walk] [Minimum Length in Miles] [Maximum Length in Miles] [Level of Difficult]".encode("utf-8"))
        

    conn.close()


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("localhost", 12345))
server_socket.listen(5)

while True:
    conn, addr = server_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(conn, addr))
    client_thread.start()
