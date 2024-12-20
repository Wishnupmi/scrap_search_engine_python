import requests
from bs4 import BeautifulSoup
import urllib.parse

# Fungsi untuk melakukan pencarian menggunakan Google dan scraping hasilnya
def google_search_scraping(query, max_results):
    results = []
    start_index = 0  # Mulai dari halaman pertama
    while len(results) < max_results:
        # URL pencarian Google, kita menggunakan URL yang telah dienkode
        query_encoded = urllib.parse.quote_plus(query)
        url = f"https://www.google.com/search?q={query_encoded}&start={start_index}"

        # Headers untuk menghindari deteksi bot oleh Google
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        try:
            # Mengirimkan permintaan ke Google
            response = requests.get(url, headers=headers)

            # Mengecek apakah request berhasil
            if response.status_code == 200:
                # Menggunakan BeautifulSoup untuk memparsing halaman HTML
                soup = BeautifulSoup(response.text, 'html.parser')

                # Mencari elemen-elemen yang berisi hasil pencarian
                search_results = soup.find_all('div', class_='tF2Cxc')

                for result in search_results:
                    if len(results) >= max_results:
                        break  # Berhenti jika sudah mencapai jumlah maksimum yang diminta

                    # Mendapatkan judul halaman
                    title = result.find('h3').text if result.find('h3') else 'No title'
                    # Mendapatkan link halaman
                    link = result.find('a')['href'] if result.find('a') else 'No link'

                    # Mendapatkan snippet (menggunakan class yang lebih umum)
                    snippet = result.find('div', class_='IsZvec')
                    if snippet:
                        snippet = snippet.get_text()  # Menyaring teks dari div tersebut
                    else:
                        snippet = "No snippet available"

                    results.append({
                        'title': title,
                        'link': link,
                        'snippet': snippet
                    })

                if len(search_results) == 0:
                    print("No more results found.")
                    break  # Keluar jika tidak ada hasil di halaman berikutnya

            else:
                print(f"Failed to retrieve the page. Status code: {response.status_code}")
                break  # Keluar jika respons gagal

        except requests.exceptions.RequestException as e:
            # Menangani error yang terjadi saat melakukan request
            print(f"An error occurred while making the request: {e}")
            break  # Keluar dari loop jika ada error

        start_index += 10  # Pindah ke halaman berikutnya

    # Menampilkan hasil pencarian
    for idx, result in enumerate(results, start=1):
        print(f"{idx}. {result['title']}")
        print(f"   URL: {result['link']}")
        print(f"   Snippet: {result['snippet']}\n")

# Fungsi utama untuk meminta input dari pengguna dan menjalankan pencarian
def main():
    # Menerima keyword pencarian dari pengguna
    query = input("Enter search query: ")

    # Menerima input jumlah hasil yang ingin ditampilkan dari pengguna
    try:
        max_results = int(input("Enter the number of search results to display: "))
    except ValueError:
        print("Please enter a valid number.")
        return

    # Memastikan bahwa pengguna memasukkan kata kunci yang tidak kosong
    if query.strip() and max_results > 0:
        google_search_scraping(query, max_results)
    else:
        print("Please enter a valid search query and number of results.")

# Menjalankan program utama
if __name__ == "__main__":
    main()
