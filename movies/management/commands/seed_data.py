import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.text import slugify
from movies.models import Category, Genre, Video, Episode, Comment, Watchlist, Rating


class Command(BaseCommand):
    help = 'Seeds the database with initial data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')

        # Create categories
        self.create_categories()

        # Create genres
        self.create_genres()

        # Create videos (movies, series, cartoons)
        self.create_videos()

        # Create demo user
        self.create_demo_user()

        self.stdout.write(self.style.SUCCESS('Data seeding completed successfully!'))

    def create_categories(self):
        categories = [
            {'name': 'Featured', 'slug': 'featured'},
            {'name': 'New Releases', 'slug': 'new-releases'},
            {'name': 'Popular', 'slug': 'popular'},
            {'name': 'Top Rated', 'slug': 'top-rated'},
        ]

        for category_data in categories:
            Category.objects.get_or_create(
                slug=category_data['slug'],
                defaults={'name': category_data['name']}
            )

        self.stdout.write(f'Created {len(categories)} categories')

    def create_genres(self):
        genres = [
            'Action', 'Adventure', 'Animation', 'Comedy', 'Crime', 'Documentary',
            'Drama', 'Fantasy', 'Horror', 'Mystery', 'Romance', 'Sci-Fi',
            'Thriller', 'Western', 'Biography', 'History', 'War', 'Musical'
        ]

        for genre_name in genres:
            Genre.objects.get_or_create(
                slug=slugify(genre_name),
                defaults={'name': genre_name}
            )

        self.stdout.write(f'Created {len(genres)} genres')

    def create_videos(self):
        # Get all categories and genres
        categories = list(Category.objects.all())
        genres = list(Genre.objects.all())

        # Movies data
        movies_data = [
            {
                'title': 'Inception',
                'description': 'A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.',
                'release_year': 2010,
                'duration': '2h 28m',
                'rating': 8.8,
                'director': 'Christopher Nolan',
                'cast': 'Leonardo DiCaprio, Joseph Gordon-Levitt, Ellen Page, Tom Hardy',
                'video_url': 'https://ok.ru/videoembed/2289155315326',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BMjAxMzY3NjcxNF5BMl5BanBnXkFtZTcwNTI5OTM0Mw@@._V1_.jpg',
                'backdrop_url': 'https://wallpaperaccess.com/full/1264514.jpg',
                'content_type': 'movie',
                'is_featured': True,
                'genres': ['Sci-Fi', 'Action', 'Adventure']
            },
            {
                'title': 'The Dark Knight',
                'description': 'When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.',
                'release_year': 2008,
                'duration': '2h 32m',
                'rating': 9.0,
                'director': 'Christopher Nolan',
                'cast': 'Christian Bale, Heath Ledger, Aaron Eckhart, Michael Caine',
                'video_url': 'https://ok.ru/videoembed/2289155315326',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BMTMxNTMwODM0NF5BMl5BanBnXkFtZTcwODAyMTk2Mw@@._V1_.jpg',
                'backdrop_url': 'https://wallpapercave.com/wp/wp2162756.jpg',
                'content_type': 'movie',
                'is_featured': True,
                'genres': ['Action', 'Crime', 'Drama']
            },
            {
                'title': 'Interstellar',
                'description': 'A team of explorers travel through a wormhole in space in an attempt to ensure humanity\'s survival.',
                'release_year': 2014,
                'duration': '2h 49m',
                'rating': 8.6,
                'director': 'Christopher Nolan',
                'cast': 'Matthew McConaughey, Anne Hathaway, Jessica Chastain',
                'video_url': 'https://ok.ru/videoembed/2289155315326',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BZjdkOTU3MDktN2IxOS00OGEyLWFmMjktY2FiMmZkNWIyODZiXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_.jpg',
                'backdrop_url': 'https://wallpapercave.com/wp/wp1817955.jpg',
                'content_type': 'movie',
                'is_featured': True,
                'genres': ['Sci-Fi', 'Adventure', 'Drama']
            },
            {
                'title': 'Avengers: Endgame',
                'description': 'After the devastating events of Avengers: Infinity War, the universe is in ruins. With the help of remaining allies, the Avengers assemble once more in order to reverse Thanos\' actions and restore balance to the universe.',
                'release_year': 2019,
                'duration': '3h 1m',
                'rating': 8.4,
                'director': 'Anthony Russo, Joe Russo',
                'cast': 'Robert Downey Jr., Chris Evans, Mark Ruffalo, Chris Hemsworth',
                'video_url': 'https://ok.ru/videoembed/2289155315326',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BMTc5MDE2ODcwNV5BMl5BanBnXkFtZTgwMzI2NzQ2NzM@._V1_.jpg',
                'backdrop_url': 'https://wallpapercave.com/wp/wp4676582.jpg',
                'content_type': 'movie',
                'is_featured': True,
                'is_popular': True,
                'genres': ['Action', 'Adventure', 'Drama']
            },
            {
                'title': 'The Matrix',
                'description': 'A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.',
                'release_year': 1999,
                'duration': '2h 16m',
                'rating': 8.7,
                'director': 'Lana Wachowski, Lilly Wachowski',
                'cast': 'Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss',
                'video_url': 'https://ok.ru/videoembed/2289155315326',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BNzQzOTk3OTAtNDQ0Zi00ZTVkLWI0MTEtMDllZjNkYzNjNTc4L2ltYWdlXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_.jpg',
                'backdrop_url': 'https://wallpapercave.com/wp/wp2757874.jpg',
                'content_type': 'movie',
                'is_popular': True,
                'genres': ['Action', 'Sci-Fi']
            },
            {
                'title': 'Mulan',
                'description': 'A young Chinese maiden disguises herself as a male warrior in order to save her father.',
                'release_year': 2020,
                'duration': '1h 55m',
                'rating': 5.7,
                'director': 'Niki Caro',
                'cast': 'Yifei Liu, Donnie Yen, Jet Li',
                'video_url': 'https://ok.ru/videoembed/2289155315326',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BNDliY2E1MjUtNzZkOS00MzJlLTgyOGEtZDg4MTI1NzZkMTBhXkEyXkFqcGdeQXVyNjMwMzc3MjE@._V1_.jpg',
                'backdrop_url': 'https://wallpapercave.com/wp/wp7042210.jpg',
                'content_type': 'movie',
                'is_new_release': True,
                'genres': ['Action', 'Adventure', 'Drama']
            },
            {
                'title': 'Soul',
                'description': 'A musician who has lost his passion for music is transported out of his body and must find his way back with the help of an infant soul learning about herself.',
                'release_year': 2020,
                'duration': '1h 40m',
                'rating': 8.1,
                'director': 'Pete Docter',
                'cast': 'Jamie Foxx, Tina Fey, Graham Norton',
                'video_url': 'https://ok.ru/videoembed/2289155315326',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BZGE1MDg5M2MtNTkyZS00MTY5LTg1YzUtZTlhZmM1Y2EwNmFmXkEyXkFqcGdeQXVyNjA3OTI0MDc@._V1_.jpg',
                'backdrop_url': 'https://wallpapercave.com/wp/wp8213270.jpg',
                'content_type': 'cartoon',
                'is_new_release': True,
                'genres': ['Animation', 'Adventure', 'Comedy']
            },
            {
                'title': 'Joker',
                'description': 'In Gotham City, mentally troubled comedian Arthur Fleck is disregarded and mistreated by society. He then embarks on a downward spiral of revolution and bloody crime. This path brings him face-to-face with his alter-ego: the Joker.',
                'release_year': 2019,
                'duration': '2h 2m',
                'rating': 8.4,
                'director': 'Todd Phillips',
                'cast': 'Joaquin Phoenix, Robert De Niro, Zazie Beetz',
                'video_url': 'https://ok.ru/videoembed/2289155315326',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BNGVjNWI4ZGUtNzE0MS00YTJmLWE0ZDctN2ZiYTk2YmI3NTYyXkEyXkFqcGdeQXVyMTkxNjUyNQ@@._V1_.jpg',
                'backdrop_url': 'https://wallpapercave.com/wp/wp4600209.jpg',
                'content_type': 'movie',
                'is_popular': True,
                'genres': ['Crime', 'Drama', 'Thriller']
            },
            {
                'title': 'Parasite',
                'description': 'Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan.',
                'release_year': 2019,
                'duration': '2h 12m',
                'rating': 8.6,
                'director': 'Bong Joon Ho',
                'cast': 'Kang-ho Song, Sun-kyun Lee, Yeo-jeong Jo',
                'video_url': 'https://ok.ru/videoembed/2289155315326',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BYWZjMjk3ZTItODQ2ZC00NTY5LWE0ZDYtZTI3MjcwN2Q5NTVkXkEyXkFqcGdeQXVyODk4OTc3MTY@._V1_.jpg',
                'backdrop_url': 'https://wallpapercave.com/wp/wp5294642.jpg',
                'content_type': 'movie',
                'is_featured': True,
                'genres': ['Comedy', 'Drama', 'Thriller']
            },
            {
                'title': 'Spider-Man: Into the Spider-Verse',
                'description': 'Teen Miles Morales becomes the Spider-Man of his universe, and must join with five spider-powered individuals from other dimensions to stop a threat for all realities.',
                'release_year': 2018,
                'duration': '1h 57m',
                'rating': 8.4,
                'director': 'Bob Persichetti, Peter Ramsey, Rodney Rothman',
                'cast': 'Shameik Moore, Jake Johnson, Hailee Steinfeld',
                'video_url': 'https://ok.ru/videoembed/2289155315326',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BMjMwNDkxMTgzOF5BMl5BanBnXkFtZTgwNTkwNTQ3NjM@._V1_.jpg',
                'backdrop_url': 'https://wallpapercave.com/wp/wp3913450.jpg',
                'content_type': 'cartoon',
                'is_popular': True,
                'genres': ['Animation', 'Action', 'Adventure']
            },
        ]

        # Series data
        series_data = [
            {
                'title': 'Star Wars: The Mandalorian',
                'description': 'The travels of a lone bounty hunter in the outer reaches of the galaxy, far from the authority of the New Republic.',
                'release_year': 2019,
                'duration': '3 Seasons',
                'rating': 8.7,
                'director': 'Jon Favreau',
                'cast': 'Pedro Pascal, Carl Weathers, Giancarlo Esposito',
                'video_url': 'https://ok.ru/videoembed/2289155315326',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BZDhlMzY0ZGItZTcyNS00ZTAxLWIyMmYtZGQ2ODg5OWZiYmJkXkEyXkFqcGdeQXVyODkzNTgxMDg@._V1_.jpg',
                'backdrop_url': 'https://wallpapercave.com/wp/wp5127149.jpg',
                'content_type': 'series',
                'is_featured': True,
                'is_popular': True,
                'genres': ['Action', 'Adventure', 'Fantasy'],
                'episodes': [
                    {
                        'title': 'Chapter 1: The Mandalorian',
                        'season_number': 1,
                        'episode_number': 1,
                        'description': 'A Mandalorian bounty hunter tracks a target for a well-paying client.',
                        'video_url': 'https://ok.ru/videoembed/2289155315326',
                        'poster_url': 'https://m.media-amazon.com/images/M/MV5BZDhlMzY0ZGItZTcyNS00ZTAxLWIyMmYtZGQ2ODg5OWZiYmJkXkEyXkFqcGdeQXVyODkzNTgxMDg@._V1_.jpg',
                        'duration': '39m',
                        'release_date': '2019-11-12'
                    },
                    {
                        'title': 'Chapter 2: The Child',
                        'season_number': 1,
                        'episode_number': 2,
                        'description': 'Target in hand, the Mandalorian must now contend with scavengers.',
                        'video_url': 'https://ok.ru/videoembed/2289155315326',
                        'poster_url': 'https://m.media-amazon.com/images/M/MV5BZDhlMzY0ZGItZTcyNS00ZTAxLWIyMmYtZGQ2ODg5OWZiYmJkXkEyXkFqcGdeQXVyODkzNTgxMDg@._V1_.jpg',
                        'duration': '32m',
                        'release_date': '2019-11-15'
                    },
                    {
                        'title': 'Chapter 3: The Sin',
                        'season_number': 1,
                        'episode_number': 3,
                        'description': 'The battered Mandalorian returns to his client for reward.',
                        'video_url': 'https://ok.ru/videoembed/2289155315326',
                        'poster_url': 'https://m.media-amazon.com/images/M/MV5BZDhlMzY0ZGItZTcyNS00ZTAxLWIyMmYtZGQ2ODg5OWZiYmJkXkEyXkFqcGdeQXVyODkzNTgxMDg@._V1_.jpg',
                        'duration': '37m',
                        'release_date': '2019-11-22'
                    },
                ]
            },
            {
                'title': 'Stranger Things',
                'description': 'When a young boy disappears, his mother, a police chief, and his friends must confront terrifying supernatural forces in order to get him back.',
                'release_year': 2016,
                'duration': '4 Seasons',
                'rating': 8.7,
                'director': 'The Duffer Brothers',
                'cast': 'Millie Bobby Brown, Finn Wolfhard, Winona Ryder',
                'video_url': 'https://ok.ru/videoembed/2289155315326',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BN2ZmYjg1YmItNWQ4OC00YWM0LWE0ZDktYThjOTZiZjhhN2Q2XkEyXkFqcGdeQXVyNjgxNTQ3Mjk@._V1_.jpg',
                'backdrop_url': 'https://wallpapercave.com/wp/wp1917154.jpg',
                'content_type': 'series',
                'is_popular': True,
                'genres': ['Drama', 'Fantasy', 'Horror'],
                'episodes': [
                    {
                        'title': 'Chapter One: The Vanishing of Will Byers',
                        'season_number': 1,
                        'episode_number': 1,
                        'description': 'On his way home from a friend\'s house, young Will sees something terrifying. Nearby, a sinister secret lurks in the depths of a government lab.',
                        'video_url': 'https://ok.ru/videoembed/2289155315326',
                        'poster_url': 'https://m.media-amazon.com/images/M/MV5BN2ZmYjg1YmItNWQ4OC00YWM0LWE0ZDktYThjOTZiZjhhN2Q2XkEyXkFqcGdeQXVyNjgxNTQ3Mjk@._V1_.jpg',
                        'duration': '47m',
                        'release_date': '2016-07-15'
                    },
                    {
                        'title': 'Chapter Two: The Weirdo on Maple Street',
                        'season_number': 1,
                        'episode_number': 2,
                        'description': 'Lucas, Mike and Dustin try to talk to the girl they found in the woods. Hopper questions an anxious  \'Lucas, Mike and Dustin try to talk to the girl they found in the woods. Hopper questions an anxious Joyce about an unsettling phone call.',
                        'video_url': 'https://ok.ru/videoembed/2289155315326',
                        'poster_url': 'https://m.media-amazon.com/images/M/MV5BN2ZmYjg1YmItNWQ4OC00YWM0LWE0ZDktYThjOTZiZjhhN2Q2XkEyXkFqcGdeQXVyNjgxNTQ3Mjk@._V1_.jpg',
                        'duration': '55m',
                        'release_date': '2016-07-15'
                    },
                ]
            },
            {
                'title': 'Breaking Bad',
                'description': 'A high school chemistry teacher diagnosed with inoperable lung cancer turns to manufacturing and selling methamphetamine in order to secure his family\'s future.',
                'release_year': 2008,
                'duration': '5 Seasons',
                'rating': 9.5,
                'director': 'Vince Gilligan',
                'cast': 'Bryan Cranston, Aaron Paul, Anna Gunn',
                'video_url': 'https://ok.ru/videoembed/2289155315326',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BYmQ4YWMxYjUtNjZmYi00MDQ1LWFjMjMtNjA5ZDdiYjdiODU5XkEyXkFqcGdeQXVyMTMzNDExODE5._V1_.jpg',
                'backdrop_url': 'https://wallpapercave.com/wp/wp1812212.jpg',
                'content_type': 'series',
                'is_featured': True,
                'genres': ['Crime', 'Drama', 'Thriller'],
                'episodes': [
                    {
                        'title': 'Pilot',
                        'season_number': 1,
                        'episode_number': 1,
                        'description': 'A high school chemistry teacher is diagnosed with terminal lung cancer and turns to a life of crime.',
                        'video_url': 'https://ok.ru/videoembed/2289155315326',
                        'poster_url': 'https://m.media-amazon.com/images/M/MV5BYmQ4YWMxYjUtNjZmYi00MDQ1LWFjMjMtNjA5ZDdiYjdiODU5XkEyXkFqcGdeQXVyMTMzNDExODE5._V1_.jpg',
                        'duration': '58m',
                        'release_date': '2008-01-20'
                    },
                    {
                        'title': 'Cat\'s in the Bag...',
                        'season_number': 1,
                        'episode_number': 2,
                        'description': 'Walt and Jesse attempt to dispose of the bodies of two rivals, but they don\'t find the task as simple as they had hoped.',
                        'video_url': 'https://ok.ru/videoembed/2289155315326',
                        'poster_url': 'https://m.media-amazon.com/images/M/MV5BYmQ4YWMxYjUtNjZmYi00MDQ1LWFjMjMtNjA5ZDdiYjdiODU5XkEyXkFqcGdeQXVyMTMzNDExODE5._V1_.jpg',
                        'duration': '48m',
                        'release_date': '2008-01-27'
                    },
                ]
            },
            {
                'title': 'Game of Thrones',
                'description': 'Nine noble families fight for control over the lands of Westeros, while an ancient enemy returns after being dormant for millennia.',
                'release_year': 2011,
                'duration': '8 Seasons',
                'rating': 9.2,
                'director': 'David Benioff, D.B. Weiss',
                'cast': 'Emilia Clarke, Peter Dinklage, Kit Harington',
                'video_url': 'https://ok.ru/videoembed/2289155315326',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BYTRiNDQwYzAtMzVlZS00NTI5LWJjYjUtMzkwNTUzMWMxZTllXkEyXkFqcGdeQXVyNDIzMzcwNjc@._V1_.jpg',
                'backdrop_url': 'https://wallpapercave.com/wp/wp1917157.jpg',
                'content_type': 'series',
                'is_popular': True,
                'genres': ['Action', 'Adventure', 'Drama'],
                'episodes': [
                    {
                        'title': 'Winter Is Coming',
                        'season_number': 1,
                        'episode_number': 1,
                        'description': 'Ned Stark, Lord of Winterfell learns that his mentor, Jon Arryn, has died and that King Robert is on his way north to offer Ned Arryn\'s position as the King\'s Hand.',
                        'video_url': 'https://ok.ru/videoembed/2289155315326',
                        'poster_url': 'https://m.media-amazon.com/images/M/MV5BYTRiNDQwYzAtMzVlZS00NTI5LWJjYjUtMzkwNTUzMWMxZTllXkEyXkFqcGdeQXVyNDIzMzcwNjc@._V1_.jpg',
                        'duration': '62m',
                        'release_date': '2011-04-17'
                    },
                    {
                        'title': 'The Kingsroad',
                        'season_number': 1,
                        'episode_number': 2,
                        'description': 'While Bran recovers from his fall, Ned takes only his daughters to King\'s Landing. Jon Snow goes with his uncle Benjen to the Wall.',
                        'video_url': 'https://ok.ru/videoembed/2289155315326',
                        'poster_url': 'https://m.media-amazon.com/images/M/MV5BYTRiNDQwYzAtMzVlZS00NTI5LWJjYjUtMzkwNTUzMWMxZTllXkEyXkFqcGdeQXVyNDIzMzcwNjc@._V1_.jpg',
                        'duration': '56m',
                        'release_date': '2011-04-24'
                    },
                ]
            },
            {
                'title': 'The Witcher',
                'description': 'Geralt of Rivia, a solitary monster hunter, struggles to find his place in a world where people often prove more wicked than beasts.',
                'release_year': 2019,
                'duration': '2 Seasons',
                'rating': 8.2,
                'director': 'Lauren Schmidt Hissrich',
                'cast': 'Henry Cavill, Freya Allan, Anya Chalotra',
                'video_url': 'https://ok.ru/videoembed/2289155315326',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BN2FiOWU4YzYtMzZiOS00MzcyLTlkOGEtOTgwZmEwMzAxMzA3XkEyXkFqcGdeQXVyMTkxNjUyNQ@@._V1_.jpg',
                'backdrop_url': 'https://wallpapercave.com/wp/wp5158249.jpg',
                'content_type': 'series',
                'is_new_release': True,
                'genres': ['Action', 'Adventure', 'Fantasy'],
                'episodes': [
                    {
                        'title': 'The End\'s Beginning',
                        'season_number': 1,
                        'episode_number': 1,
                        'description': 'Hostile townsfolk and a cunning mage greet Geralt in the town of Blaviken. Ciri finds her royal world upended when Nilfgaard sets its sights on Cintra.',
                        'video_url': 'https://ok.ru/videoembed/2289155315326',
                        'poster_url': 'https://m.media-amazon.com/images/M/MV5BN2FiOWU4YzYtMzZiOS00MzcyLTlkOGEtOTgwZmEwMzAxMzA3XkEyXkFqcGdeQXVyMTkxNjUyNQ@@._V1_.jpg',
                        'duration': '61m',
                        'release_date': '2019-12-20'
                    },
                    {
                        'title': 'Four Marks',
                        'season_number': 1,
                        'episode_number': 2,
                        'description': 'Bullied and neglected, Yennefer accidentally finds a means of escape. Geralt\'s hunt for a so-called devil goes to hell. Ciri seeks safety in numbers.',
                        'video_url': 'https://ok.ru/videoembed/2289155315326',
                        'poster_url': 'https://m.media-amazon.com/images/M/MV5BN2FiOWU4YzYtMzZiOS00MzcyLTlkOGEtOTgwZmEwMzAxMzA3XkEyXkFqcGdeQXVyMTkxNjUyNQ@@._V1_.jpg',
                        'duration': '61m',
                        'release_date': '2019-12-20'
                    },
                ]
            },
        ]

        # Create movies
        for movie_data in movies_data:
            # Get genre objects
            movie_genres = []
            for genre_name in movie_data.pop('genres', []):
                genre = Genre.objects.filter(name=genre_name).first()
                if genre:
                    movie_genres.append(genre)

            # Create slug
            slug = slugify(movie_data['title'])
            self.stdout.write(f"Poster: {movie_data['poster_url']}")
            # Create movie
            movie, created = Video.objects.get_or_create(
                slug=slug,
                defaults={**movie_data}
            )
            # Add genres
            movie.genres.set(movie_genres)
            self.stdout.write(f"Poster: {movie.poster_url}")
            # Add to categories
            if movie.is_featured:
                featured_category = Category.objects.get(slug='featured')
                movie.categories.add(featured_category)

            if movie.is_new_release:
                new_releases_category = Category.objects.get(slug='new-releases')
                movie.categories.add(new_releases_category)

            if movie.is_popular:
                popular_category = Category.objects.get(slug='popular')
                movie.categories.add(popular_category)

            if created:
                self.stdout.write(f'Created movie: {movie.title}')
            else:
                self.stdout.write(f'Updated movie: {movie.title}')

        # Create series
        for series_data in series_data:
            # Get genre objects
            series_genres = []
            for genre_name in series_data.pop('genres', []):
                genre = Genre.objects.filter(name=genre_name).first()
                if genre:
                    series_genres.append(genre)

            # Get episodes data
            episodes_data = series_data.pop('episodes', [])

            # Create slug
            slug = slugify(series_data['title'])

            # Create series
            series, created = Video.objects.get_or_create(
                slug=slug,
                defaults={**series_data}
            )

            # Add genres
            series.genres.set(series_genres)

            # Add to categories
            if series.is_featured:
                featured_category = Category.objects.get(slug='featured')
                series.categories.add(featured_category)

            if series.is_new_release:
                new_releases_category = Category.objects.get(slug='new-releases')
                series.categories.add(new_releases_category)

            if series.is_popular:
                popular_category = Category.objects.get(slug='popular')
                series.categories.add(popular_category)

            # Create episodes
            for episode_data in episodes_data:
                episode_slug = slugify(
                    f"{series.title}-s{episode_data['season_number']}e{episode_data['episode_number']}")

                episode, episode_created = Episode.objects.get_or_create(
                    series=series,
                    season_number=episode_data['season_number'],
                    episode_number=episode_data['episode_number'],
                    defaults={
                        'title': episode_data['title'],
                        'slug': episode_slug,
                        'description': episode_data['description'],
                        'video_url': episode_data['video_url'],
                        'poster_url': episode_data.get('poster_url', ''),
                        'duration': episode_data['duration'],
                        'release_date': episode_data['release_date'],
                    }
                )

                if episode_created:
                    self.stdout.write(f'Created episode: {episode.title} for {series.title}')

            if created:
                self.stdout.write(f'Created series: {series.title}')
            else:
                self.stdout.write(f'Updated series: {series.title}')

    def create_demo_user(self):
        # Create demo user
        demo_user, created = User.objects.get_or_create(
            username='demo',
            defaults={
                'email': 'demo@example.com',
                'first_name': 'Demo',
                'last_name': 'User',
                'is_active': True
            }
        )

        if created:
            demo_user.set_password('demo1234')
            demo_user.save()
            self.stdout.write('Created demo user')

        # Add some videos to demo user's watchlist
        videos = Video.objects.all()
        for video in random.sample(list(videos), min(3, len(videos))):
            Watchlist.objects.get_or_create(user=demo_user, video=video)

        # Add some ratings
        for video in random.sample(list(videos), min(2, len(videos))):
            Rating.objects.get_or_create(
                user=demo_user,
                video=video,
                defaults={
                    'value': random.randint(7, 10)
                }
            )

        # Add some comments
        for video in random.sample(list(videos), min(2, len(videos))):
            Comment.objects.get_or_create(
                user=demo_user,
                video=video,
                defaults={
                    'content': f'Bu {video.title} juda ham ajoyib! Menga juda yoqdi.'
                }
            )

        self.stdout.write('Added watchlist items, ratings, and comments for demo user')
