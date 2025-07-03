import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.text import slugify
from movies.models import Category, Genre, Video, Episode, Comment


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
        # self.create_demo_user()

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
            'Thriller', 'Western', 'Biography', 'History', 'War', 'Musical',
            'Family', 'Sport', 'Superhero', 'Psychological', 'Dystopian'
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
            # Original movies
            {
                'title': 'Inception',
                'description': 'A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.',
                'cast': 'Leonardo DiCaprio, Joseph Gordon-Levitt, Ellen Page, Tom Hardy',
                'video_url': 'https://ok.ru/videoembed/2289155315326',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BMjAxMzY3NjcxNF5BMl5BanBnXkFtZTcwNTI5OTM0Mw@@._V1_.jpg',
                'content_type': 'movie',
                'is_featured': True,
                'genres': ['Sci-Fi', 'Action', 'Adventure']
            },
            {
                'title': 'The Dark Knight',
                'description': 'When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.',
                'cast': 'Christian Bale, Heath Ledger, Aaron Eckhart, Michael Caine',
                'video_url': 'https://ok.ru/videoembed/2289155315326',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BMTMxNTMwODM0NF5BMl5BanBnXkFtZTcwODAyMTk2Mw@@._V1_.jpg',
                'content_type': 'movie',
                'is_featured': True,
                'genres': ['Action', 'Crime', 'Drama']
            },
            {
                'title': 'Interstellar',
                'description': 'A team of explorers travel through a wormhole in space in an attempt to ensure humanity\'s survival.',
                'cast': 'Matthew McConaughey, Anne Hathaway, Jessica Chastain',
                'video_url': 'https://ok.ru/videoembed/2289155315326',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BZjdkOTU3MDktN2IxOS00OGEyLWFmMjktY2FiMmZkNWIyODZiXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_.jpg',
                'content_type': 'movie',
                'is_featured': True,
                'genres': ['Sci-Fi', 'Adventure', 'Drama']
            },
            {
                'title': 'Avengers: Endgame',
                'description': 'After the devastating events of Avengers: Infinity War, the universe is in ruins. With the help of remaining allies, the Avengers assemble once more in order to reverse Thanos\' actions and restore balance to the universe.',
                'cast': 'Robert Downey Jr., Chris Evans, Mark Ruffalo, Chris Hemsworth',
                'video_url': 'https://ok.ru/videoembed/2289155315326',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BMTc5MDE2ODcwNV5BMl5BanBnXkFtZTgwMzI2NzQ2NzM@._V1_.jpg',
                'content_type': 'movie',
                'is_featured': True,
                'is_popular': True,
                'genres': ['Action', 'Adventure', 'Drama']
            },
            {
                'title': 'The Matrix',
                'description': 'A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.',
                'cast': 'Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss',
                'video_url': 'https://ok.ru/videoembed/2289155315326',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BNzQzOTk3OTAtNDQ0Zi00ZTVkLWI0MTEtMDllZjNkYzNjNTc4L2ltYWdlXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_.jpg',
                'content_type': 'movie',
                'is_popular': True,
                'genres': ['Action', 'Sci-Fi']
            },
            {
                'title': 'Mulan',
                'description': 'A young Chinese maiden disguises herself as a male warrior in order to save her father.',
                'cast': 'Yifei Liu, Donnie Yen, Jet Li',
                'video_url': 'https://ok.ru/videoembed/2289155315326',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BNDliY2E1MjUtNzZkOS00MzJlLTgyOGEtZDg4MTI1NzZkMTBhXkEyXkFqcGdeQXVyNjMwMzc3MjE@._V1_.jpg',
                'content_type': 'movie',
                'is_new_release': True,
                'genres': ['Action', 'Adventure', 'Drama']
            },
            {
                'title': 'Soul',
                'description': 'A musician who has lost his passion for music is transported out of his body and must find his way back with the help of an infant soul learning about herself.',
                'cast': 'Jamie Foxx, Tina Fey, Graham Norton',
                'video_url': 'https://ok.ru/videoembed/2289155315326',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BZGE1MDg5M2MtNTkyZS00MTY5LTg1YzUtZTlhZmM1Y2EwNmFmXkEyXkFqcGdeQXVyNjA3OTI0MDc@._V1_.jpg',
                'content_type': 'cartoon',
                'is_new_release': True,
                'genres': ['Animation', 'Adventure', 'Comedy']
            },
            {
                'title': 'Joker',
                'description': 'In Gotham City, mentally troubled comedian Arthur Fleck is disregarded and mistreated by society. He then embarks on a downward spiral of revolution and bloody crime. This path brings him face-to-face with his alter-ego: the Joker.',
                'cast': 'Joaquin Phoenix, Robert De Niro, Zazie Beetz',
                'video_url': 'https://ok.ru/videoembed/2289155315326',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BNGVjNWI4ZGUtNzE0MS00YTJmLWE0ZDctN2ZiYTk2YmI3NTYyXkEyXkFqcGdeQXVyMTkxNjUyNQ@@._V1_.jpg',
                'content_type': 'movie',
                'is_popular': True,
                'genres': ['Crime', 'Drama', 'Thriller']
            },
            {
                'title': 'Parasite',
                'description': 'Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan.',
                'cast': 'Kang-ho Song, Sun-kyun Lee, Yeo-jeong Jo',
                'video_url': 'https://ok.ru/videoembed/2289155315326',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BYWZjMjk3ZTItODQ2ZC00NTY5LWE0ZDYtZTI3MjcwN2Q5NTVkXkEyXkFqcGdeQXVyODk4OTc3MTY@._V1_.jpg',
                'content_type': 'movie',
                'is_featured': True,
                'genres': ['Comedy', 'Drama', 'Thriller']
            },
            {
                'title': 'Spider-Man: Into the Spider-Verse',
                'description': 'Teen Miles Morales becomes the Spider-Man of his universe, and must join with five spider-powered individuals from other dimensions to stop a threat for all realities.',
                'cast': 'Shameik Moore, Jake Johnson, Hailee Steinfeld',
                'video_url': 'https://ok.ru/videoembed/2289155315326',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BMjMwNDkxMTgzOF5BMl5BanBnXkFtZTgwNTkwNTQ3NjM@._V1_.jpg',
                'content_type': 'cartoon',
                'is_popular': True,
                'genres': ['Animation', 'Action', 'Adventure']
            },

            # Additional movies
            {
                'title': 'The Shawshank Redemption',
                'description': 'Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.',
                'cast': 'Tim Robbins, Morgan Freeman, Bob Gunton',
                'video_url': 'https://ok.ru/videoembed/2289155315326',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BMDFkYTc0MGEtZmNhMC00ZDIzLWFmNTEtODM1ZmRlYWMwMWFmXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_.jpg',
                'content_type': 'movie',
                'is_featured': True,
                'genres': ['Drama']
            },
            {
                'title': 'The Godfather',
                'description': 'The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.',
                'cast': 'Marlon Brando, Al Pacino, James Caan',
                'video_url': 'https://ok.ru/videoembed/2289155315326',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BM2MyNjYxNmUtYTAwNi00MTYxLWJmNWYtYzZlODY3ZTk3OTFlXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_.jpg',
                'content_type': 'movie',
                'is_popular': True,
                'genres': ['Crime', 'Drama']
            },
            {
                'title': 'Pulp Fiction',
                'description': 'The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption.',
                'cast': 'John Travolta, Uma Thurman, Samuel L. Jackson',
                'video_url': 'https://ok.ru/videoembed/2289155315326',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BNGNhMDIzZTUtNTBlZi00MTRlLWFjM2ItYzViMjE3YzI5MjljXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_.jpg',
                'content_type': 'movie',
                'is_featured': True,
                'genres': ['Crime', 'Drama']
            },
            {
                'title': 'The Lord of the Rings: The Fellowship of the Ring',
                'description': 'A meek Hobbit from the Shire and eight companions set out on a journey to destroy the powerful One Ring and save Middle-earth from the Dark Lord Sauron.',
                'cast': 'Elijah Wood, Ian McKellen, Orlando Bloom',
                'video_url': 'https://ok.ru/videoembed/2289155315326',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BN2EyZjM3NzUtNWUzMi00MTgxLWI0NTctMzY4M2VlOTdjZWRiXkEyXkFqcGdeQXVyNDUzOTQ5MjY@._V1_.jpg',
                'content_type': 'movie',
                'is_popular': True,
                'genres': ['Adventure', 'Drama', 'Fantasy']
            },
            {
                'title': 'Forrest Gump',
                'description': 'The presidencies of Kennedy and Johnson, the Vietnam War, the Watergate scandal and other historical events unfold from the perspective of an Alabama man with an IQ of 75, whose only desire is to be reunited with his childhood sweetheart.',
                'cast': 'Tom Hanks, Robin Wright, Gary Sinise',
                'video_url': 'https://ok.ru/videoembed/2289155315326',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BNWIwODRlZTUtY2U3ZS00Yzg1LWJhNzYtMmZiYmEyNmU1NjMzXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_.jpg',
                'content_type': 'movie',
                'is_featured': True,
                'genres': ['Drama', 'Romance']
            },
            {
                'title': 'Fight Club',
                'description': 'An insomniac office worker and a devil-may-care soapmaker form an underground fight club that evolves into something much, much more.',
                'cast': 'Brad Pitt, Edward Norton, Helena Bonham Carter',
                'video_url': 'https://ok.ru/videoembed/2289155315326',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BMmEzNTkxYjQtZTc0MC00YTVjLTg5ZTEtZWMwOWVlYzY0NWIwXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_.jpg',
                'content_type': 'movie',
                'is_popular': True,
                'genres': ['Drama']
            },
            {
                'title': 'Goodfellas',
                'description': 'The story of Henry Hill and his life in the mob, covering his relationship with his wife Karen Hill and his mob partners Jimmy Conway and Tommy DeVito in the Italian-American crime syndicate.',
                'cast': 'Robert De Niro, Ray Liotta, Joe Pesci',
                'video_url': 'https://ok.ru/videoembed/2289155315326',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BY2NkZjEzMDgtN2RjYy00YzM1LWI4ZmQtMjIwYjFjNmI3ZGEwXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_.jpg',
                'content_type': 'movie',
                'is_featured': True,
                'genres': ['Biography', 'Crime', 'Drama']
            },
            {
                'title': 'The Silence of the Lambs',
                'description': 'A young F.B.I. cadet must receive the help of an incarcerated and manipulative cannibal killer to help catch another serial killer, a madman who skins his victims.',
                'cast': 'Jodie Foster, Anthony Hopkins, Lawrence A. Bonney',
                'video_url': 'https://ok.ru/videoembed/2289155315326',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BNjNhZTk0ZmEtNjJhMi00YzFlLWE1MmEtYzM1M2ZmMGMwMTU4XkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_.jpg',
                'content_type': 'movie',
                'is_popular': True,
                'genres': ['Crime', 'Drama', 'Thriller']
            },
            {
                'title': 'Saving Private Ryan',
                'description': 'Following the Normandy Landings, a group of U.S. soldiers go behind enemy lines to retrieve a paratrooper whose brothers have been killed in action.',
                'cast': 'Tom Hanks, Matt Damon, Tom Sizemore',
                'video_url': 'https://ok.ru/videoembed/2289155315326',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BZjhkMDM4MWItZTVjOC00ZDRhLThmYTAtM2I5NzBmNmNlMzI1XkEyXkFqcGdeQXVyNDYyMDk5MTU@._V1_.jpg',
                'content_type': 'movie',
                'is_featured': True,
                'genres': ['Drama', 'War']
            },
            {
                'title': 'The Green Mile',
                'description': 'The lives of guards on Death Row are affected by one of their charges: a black man accused of child murder and rape, yet who has a mysterious gift.',
                'cast': 'Tom Hanks, Michael Clarke Duncan, David Morse',
                'video_url': 'https://ok.ru/videoembed/2289155315326',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BMTUxMzQyNjA5MF5BMl5BanBnXkFtZTYwOTU2NTY3._V1_.jpg',
                'content_type': 'movie',
                'is_popular': True,
                'genres': ['Crime', 'Drama', 'Fantasy']
            },
            {
                'title': 'Spirited Away',
                'description': 'During her family\'s move to the suburbs, a sullen 10-year-old girl wanders into a world ruled by gods, witches, and spirits, and where humans are changed into beasts.',
                'cast': 'Daveigh Chase, Suzanne Pleshette, Miyu Irino',
                'video_url': 'https://ok.ru/videoembed/2289155315326',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BMjlmZmI5MDctNDE2YS00YWE0LWE5ZWItZDBhYWQ0NTcxNWRhXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_.jpg',
                'content_type': 'cartoon',
                'is_featured': True,
                'genres': ['Animation', 'Adventure', 'Family']
            },
            {
                'title': 'Your Name',
                'description': 'Two strangers find themselves linked in a bizarre way. When a connection forms, will distance be the only thing to keep them apart?',
                'cast': 'Ryûnosuke Kamiki, Mone Kamishiraishi, Ryô Narita',
                'video_url': 'https://ok.ru/videoembed/2289155315326',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BODRmZDVmNzUtZDA4ZC00NjhkLWI2M2UtN2M0ZDIzNDcxYThjL2ltYWdlXkEyXkFqcGdeQXVyNTk0MzMzODA@._V1_.jpg',
                'content_type': 'cartoon',
                'is_new_release': True,
                'genres': ['Animation', 'Drama', 'Fantasy']
            },
            {
                'title': 'Demon Slayer: Mugen Train',
                'description': 'After his family was brutally murdered and his sister turned into a demon, Tanjiro Kamado\'s journey as a demon slayer began. Tanjiro and his comrades embark on a new mission aboard the Mugen Train, on track to despair.',
                'cast': 'Natsuki Hanae, Akari Kitô, Yoshitsugu Matsuoka',
                'video_url': 'https://ok.ru/videoembed/2289155315326',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BODI2NjdlYWItMTE1ZC00YzI2LTlhZGQtNzE3NzA4MWM0ODYzXkEyXkFqcGdeQXVyNjU1OTg4OTM@._V1_.jpg',
                'content_type': 'cartoon',
                'is_new_release': True,
                'genres': ['Animation', 'Action', 'Adventure']
            },
            {
                'title': 'The Lion King',
                'description': 'Lion prince Simba and his father are targeted by his bitter uncle, who wants to ascend the throne himself.',
                'cast': 'Matthew Broderick, Jeremy Irons, James Earl Jones',
                'video_url': 'https://ok.ru/videoembed/2289155315326',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BYTYxNGMyZTYtMjE3MS00MzNjLWFjNmYtMDk3N2FmM2JiM2M1XkEyXkFqcGdeQXVyNjY5NDU4NzI@._V1_.jpg',
                'content_type': 'cartoon',
                'is_popular': True,
                'genres': ['Animation', 'Adventure', 'Drama']
            },
            {
                'title': 'Toy Story',
                'description': 'A cowboy doll is profoundly threatened and jealous when a new spaceman figure supplants him as top toy in a boy\'s room.',
                'cast': 'Tom Hanks, Tim Allen, Don Rickles',
                'video_url': 'https://ok.ru/videoembed/2289155315326',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BMDU2ZWJlMjktMTRhMy00ZTA5LWEzNDgtYmNmZTEwZTViZWJkXkEyXkFqcGdeQXVyNDQ2OTk4MzI@._V1_.jpg',
                'content_type': 'cartoon',
                'is_featured': True,
                'genres': ['Animation', 'Adventure', 'Comedy']
            },
            {
                'title': 'Coco',
                'description': 'Aspiring musician Miguel, confronted with his family\'s ancestral ban on music, enters the Land of the Dead to find his great-great-grandfather, a legendary singer.',
                'cast': 'Anthony Gonzalez, Gael García Bernal, Benjamin Bratt',
                'video_url': 'https://ok.ru/videoembed/2289155315326',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BYjQ5NjM0Y2YtNjZkNC00ZDhkLWJjMWItN2QyNzFkMDE3ZjAxXkEyXkFqcGdeQXVyODIxMzk5NjA@._V1_.jpg',
                'content_type': 'cartoon',
                'is_popular': True,
                'genres': ['Animation', 'Adventure', 'Family']
            },
            {
                'title': 'Dune',
                'description': 'Feature adaptation of Frank Herbert\'s science fiction novel, about the son of a noble family entrusted with the protection of the most valuable asset and most vital element in the galaxy.',
                'cast': 'Timothée Chalamet, Rebecca Ferguson, Zendaya',
                'video_url': 'https://ok.ru/videoembed/2289155315326',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BN2FjNmEyNWMtYzM0ZS00NjIyLTg5YzYtYThlMGVjNzE1OGViXkEyXkFqcGdeQXVyMTkxNjUyNQ@@._V1_.jpg',
                'content_type': 'movie',
                'is_new_release': True,
                'genres': ['Action', 'Adventure', 'Drama']
            },
            {
                'title': 'No Time to Die',
                'description': 'James Bond has left active service. His peace is short-lived when Felix Leiter, an old friend from the CIA, turns up asking for help, leading Bond onto the trail of a mysterious villain armed with dangerous new technology.',
                'cast': 'Daniel Craig, Ana de Armas, Rami Malek',
                'video_url': 'https://ok.ru/videoembed/2289155315326',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BYWQ2NzQ1NjktMzNkNS00MGY1LTgwMmMtYTllYTI5YzNmMmE0XkEyXkFqcGdeQXVyMjM4NTM5NDY@._V1_.jpg',
                'content_type': 'movie',
                'is_new_release': True,
                'genres': ['Action', 'Adventure', 'Thriller']
            },
            {
                'title': 'The Batman',
                'description': 'When the Riddler, a sadistic serial killer, begins murdering key political figures in Gotham, Batman is forced to investigate the city\'s hidden corruption and question his family\'s involvement.',
                'cast': 'Robert Pattinson, Zoë Kravitz, Jeffrey Wright',
                'video_url': 'https://ok.ru/videoembed/2289155315326',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BMDdmMTBiNTYtMDIzNi00NGVlLWIzMDYtZTk3MTQ3NGQxZGEwXkEyXkFqcGdeQXVyMzMwOTU5MDk@._V1_.jpg',
                'content_type': 'movie',
                'is_new_release': True,
                'genres': ['Action', 'Crime', 'Drama']
            },
            {
                'title': 'Top Gun: Maverick',
                'description': 'After more than thirty years of service as one of the Navy\'s top aviators, Pete Mitchell is where he belongs, pushing the envelope as a courageous test pilot and dodging the advancement in rank that would ground him.',
                'cast': 'Tom Cruise, Jennifer Connelly, Miles Teller',
                'video_url': 'https://ok.ru/videoembed/2289155315326',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BZWYzOGEwNTgtNWU3NS00ZTQ0LWJkODUtMmVhMjIwMjA1ZmQwXkEyXkFqcGdeQXVyMjkwOTAyMDU@._V1_.jpg',
                'content_type': 'movie',
                'is_new_release': True,
                'genres': ['Action', 'Drama']
            },
            {
                'title': 'Everything Everywhere All at Once',
                'description': 'An aging Chinese immigrant is swept up in an insane adventure, where she alone can save the world by exploring other universes connecting with the lives she could have led.',
                'cast': 'Michelle Yeoh, Stephanie Hsu, Jamie Lee Curtis',
                'video_url': 'https://ok.ru/videoembed/2289155315326',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BYTdiOTIyZTQtNmQ1OS00NjZlLWIyMTgtYzk5Y2M3ZDVmMDk1XkEyXkFqcGdeQXVyMTAzMDg4NzU0._V1_.jpg',
                'content_type': 'movie',
                'is_new_release': True,
                'genres': ['Action', 'Adventure', 'Comedy']
            },
        ]

        # Series data
        series_data = [
            # Original series
            {
                'title': 'Star Wars: The Mandalorian',
                'description': 'The travels of a lone bounty hunter in the outer reaches of the galaxy, far from the authority of the New Republic.',
                'cast': 'Pedro Pascal, Carl Weathers, Giancarlo Esposito',
                'video_url': 'https://ok.ru/videoembed/2289155315326',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BZDhlMzY0ZGItZTcyNS00ZTAxLWIyMmYtZGQ2ODg5OWZiYmJkXkEyXkFqcGdeQXVyODkzNTgxMDg@._V1_.jpg',
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
                    },
                    {
                        'title': 'Chapter 2: The Child',
                        'season_number': 1,
                        'episode_number': 2,
                        'description': 'Target in hand, the Mandalorian must now contend with scavengers.',
                        'video_url': 'https://ok.ru/videoembed/2289155315326',
                        'poster_url': 'https://m.media-amazon.com/images/M/MV5BZDhlMzY0ZGItZTcyNS00ZTAxLWIyMmYtZGQ2ODg5OWZiYmJkXkEyXkFqcGdeQXVyODkzNTgxMDg@._V1_.jpg',
                    },
                    {
                        'title': 'Chapter 3: The Sin',
                        'season_number': 1,
                        'episode_number': 3,
                        'description': 'The battered Mandalorian returns to his client for reward.',
                        'video_url': 'https://ok.ru/videoembed/2289155315326',
                        'poster_url': 'https://m.media-amazon.com/images/M/MV5BZDhlMzY0ZGItZTcyNS00ZTAxLWIyMmYtZGQ2ODg5OWZiYmJkXkEyXkFqcGdeQXVyODkzNTgxMDg@._V1_.jpg',
                    },
                ]
            },
            {
                'title': 'Stranger Things',
                'description': 'When a young boy disappears, his mother, a police chief, and his friends must confront terrifying supernatural forces in order to get him back.',
                'cast': 'Millie Bobby Brown, Finn Wolfhard, Winona Ryder',
                'video_url': 'https://ok.ru/videoembed/2289155315326',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BN2ZmYjg1YmItNWQ4OC00YWM0LWE0ZDktYThjOTZiZjhhN2Q2XkEyXkFqcGdeQXVyNjgxNTQ3Mjk@._V1_.jpg',
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
                    },
                    {
                        'title': 'Chapter Two: The Weirdo on Maple Street',
                        'season_number': 1,
                        'episode_number': 2,
                        'description': 'Lucas, Mike and Dustin try to talk to the girl they found in the woods. Hopper questions an anxious  \'Lucas, Mike and Dustin try to talk to the girl they found in the woods. Hopper questions an anxious Joyce about an unsettling phone call.',
                        'video_url': 'https://ok.ru/videoembed/2289155315326',
                        'poster_url': 'https://m.media-amazon.com/images/M/MV5BN2ZmYjg1YmItNWQ4OC00YWM0LWE0ZDktYThjOTZiZjhhN2Q2XkEyXkFqcGdeQXVyNjgxNTQ3Mjk@._V1_.jpg',
                    },
                ]
            },
            {
                'title': 'Breaking Bad',
                'description': 'A high school chemistry teacher diagnosed with inoperable lung cancer turns to manufacturing and selling methamphetamine in order to secure his family\'s future.',
                'cast': 'Bryan Cranston, Aaron Paul, Anna Gunn',
                'video_url': 'https://ok.ru/videoembed/2289155315326',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BYmQ4YWMxYjUtNjZmYi00MDQ1LWFjMjMtNjA5ZDdiYjdiODU5XkEyXkFqcGdeQXVyMTMzNDExODE5._V1_.jpg',
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
                    },
                    {
                        'title': 'Cat\'s in the Bag...',
                        'season_number': 1,
                        'episode_number': 2,
                        'description': 'Walt and Jesse attempt to dispose of the bodies of two rivals, but they don\'t find the task as simple as they had hoped.',
                        'video_url': 'https://ok.ru/videoembed/2289155315326',
                        'poster_url': 'https://m.media-amazon.com/images/M/MV5BYmQ4YWMxYjUtNjZmYi00MDQ1LWFjMjMtNjA5ZDdiYjdiODU5XkEyXkFqcGdeQXVyMTMzNDExODE5._V1_.jpg',
                    },
                ]
            },
            {
                'title': 'Game of Thrones',
                'description': 'Nine noble families fight for control over the lands of Westeros, while an ancient enemy returns after being dormant for millennia.',
                'cast': 'Emilia Clarke, Peter Dinklage, Kit Harington',
                'video_url': 'https://ok.ru/videoembed/2289155315326',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BYTRiNDQwYzAtMzVlZS00NTI5LWJjYjUtMzkwNTUzMWMxZTllXkEyXkFqcGdeQXVyNDIzMzcwNjc@._V1_.jpg',
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
                    },
                    {
                        'title': 'The Kingsroad',
                        'season_number': 1,
                        'episode_number': 2,
                        'description': 'While Bran recovers from his fall, Ned takes only his daughters to King\'s Landing. Jon Snow goes with his uncle Benjen to the Wall.',
                        'video_url': 'https://ok.ru/videoembed/2289155315326',
                        'poster_url': 'https://m.media-amazon.com/images/M/MV5BYTRiNDQwYzAtMzVlZS00NTI5LWJjYjUtMzkwNTUzMWMxZTllXkEyXkFqcGdeQXVyNDIzMzcwNjc@._V1_.jpg',
                    },
                ]
            },
            {
                'title': 'The Witcher',
                'description': 'Geralt of Rivia, a solitary monster hunter, struggles to find his place in a world where people often prove more wicked than beasts.',
                'cast': 'Henry Cavill, Freya Allan, Anya Chalotra',
                'video_url': 'https://ok.ru/videoembed/2289155315326',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BN2FiOWU4YzYtMzZiOS00MzcyLTlkOGEtOTgwZmEwMzAxMzA3XkEyXkFqcGdeQXVyMTkxNjUyNQ@@._V1_.jpg',
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
                    },
                    {
                        'title': 'Four Marks',
                        'season_number': 1,
                        'episode_number': 2,
                        'description': 'Bullied and neglected, Yennefer accidentally finds a means of escape. Geralt\'s hunt for a so-called devil goes to hell. Ciri seeks safety in numbers.',
                        'video_url': 'https://ok.ru/videoembed/2289155315326',
                        'poster_url': 'https://m.media-amazon.com/images/M/MV5BN2FiOWU4YzYtMzZiOS00MzcyLTlkOGEtOTgwZmEwMzAxMzA3XkEyXkFqcGdeQXVyMTkxNjUyNQ@@._V1_.jpg',
                    },
                ]
            },

            # Additional series
            {
                'title': 'The Office',
                'description': 'A mockumentary on a group of typical office workers, where the workday consists of ego clashes, inappropriate behavior, and tedium.',
                'cast': 'Steve Carell, Jenna Fischer, John Krasinski',
                'video_url': 'https://ok.ru/videoembed/2289155315326',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BMDNkOTE4NDQtMTNmYi00MWE0LWE4ZTktYTc0NzhhNWIzNzJiXkEyXkFqcGdeQXVyMzQ2MDI5NjU@._V1_.jpg',
                'content_type': 'series',
                'is_popular': True,
                'genres': ['Comedy'],
                'episodes': [
                    {
                        'title': 'Pilot',
                        'season_number': 1,
                        'episode_number': 1,
                        'description': 'The premiere episode introduces the boss and staff of the Dunder Mifflin paper company in Scranton, Pennsylvania in a documentary about the workplace.',
                        'video_url': 'https://ok.ru/videoembed/2289155315326',
                        'poster_url': 'https://m.media-amazon.com/images/M/MV5BMDNkOTE4NDQtMTNmYi00MWE0LWE4ZTktYTc0NzhhNWIzNzJiXkEyXkFqcGdeQXVyMzQ2MDI5NjU@._V1_.jpg',
                    },
                    {
                        'title': 'Diversity Day',
                        'season_number': 1,
                        'episode_number': 2,
                        'description': 'Michael\'s off-color remark puts a sensitivity trainer in the office for a presentation, which prompts Michael to create his own.',
                        'video_url': 'https://ok.ru/videoembed/2289155315326',
                        'poster_url': 'https://m.media-amazon.com/images/M/MV5BMDNkOTE4NDQtMTNmYi00MWE0LWE4ZTktYTc0NzhhNWIzNzJiXkEyXkFqcGdeQXVyMzQ2MDI5NjU@._V1_.jpg',
                    },
                ]
            },
            {
                'title': 'Friends',
                'description': 'Follows the personal and professional lives of six twenty to thirty-something-year-old friends living in Manhattan.',
                'cast': 'Jennifer Aniston, Courteney Cox, Lisa Kudrow',
                'video_url': 'https://ok.ru/videoembed/2289155315326',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BNDVkYjU0MzctMWRmZi00NTkxLTgwZWEtOWVhYjZlYjllYmU4XkEyXkFqcGdeQXVyNTA4NzY1MzY@._V1_.jpg',
                'content_type': 'series',
                'is_featured': True,
                'genres': ['Comedy', 'Romance'],
                'episodes': [
                    {
                        'title': 'The One Where Monica Gets a Roommate',
                        'season_number': 1,
                        'episode_number': 1,
                        'description': 'Monica and the gang introduce Rachel to the "real world" after she leaves her fiancé at the altar.',
                        'video_url': 'https://ok.ru/videoembed/2289155315326',
                        'poster_url': 'https://m.media-amazon.com/images/M/MV5BNDVkYjU0MzctMWRmZi00NTkxLTgwZWEtOWVhYjZlYjllYmU4XkEyXkFqcGdeQXVyNTA4NzY1MzY@._V1_.jpg',
                    },
                    {
                        'title': 'The One with the Sonogram at the End',
                        'season_number': 1,
                        'episode_number': 2,
                        'description': 'Ross finds out his ex-wife is pregnant. Rachel returns her engagement ring to Barry. Monica becomes stressed when her and Ross\'s parents come to visit.',
                        'video_url': 'https://ok.ru/videoembed/2289155315326',
                        'poster_url': 'https://m.media-amazon.com/images/M/MV5BNDVkYjU0MzctMWRmZi00NTkxLTgwZWEtOWVhYjZlYjllYmU4XkEyXkFqcGdeQXVyNTA4NzY1MzY@._V1_.jpg',
                    },
                ]
            },
            {
                'title': 'The Crown',
                'description': 'Follows the political rivalries and romance of Queen Elizabeth II\'s reign and the events that shaped the second half of the twentieth century.',
                'cast': 'Claire Foy, Olivia Colman, Imelda Staunton',
                'video_url': 'https://ok.ru/videoembed/2289155315326',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BZmY0MzBlNjctNTRmNy00Njk3LWFjMzctMWQwZDAwMGJmY2MyXkEyXkFqcGdeQXVyMDM2NDM2MQ@@._V1_.jpg',
                'content_type': 'series',
                'is_featured': True,
                'genres': ['Biography', 'Drama', 'History'],
                'episodes': [
                    {
                        'title': 'Wolferton Splash',
                        'season_number': 1,
                        'episode_number': 1,
                        'description': 'A young Princess Elizabeth marries Prince Philip. As King George VI\'s health worsens, Winston Churchill is elected prime minister for the second time.',
                        'video_url': 'https://ok.ru/videoembed/2289155315326',
                        'poster_url': 'https://m.media-amazon.com/images/M/MV5BZmY0MzBlNjctNTRmNy00Njk3LWFjMzctMWQwZDAwMGJmY2MyXkEyXkFqcGdeQXVyMDM2NDM2MQ@@._V1_.jpg',
                    },
                    {
                        'title': 'Hyde Park Corner',
                        'season_number': 1,
                        'episode_number': 2,
                        'description': 'With King George too ill to travel, Elizabeth and Philip embark on a four-continent Commonwealth tour. Party leaders attempt to undermine Churchill.',
                        'video_url': 'https://ok.ru/videoembed/2289155315326',
                        'poster_url': 'https://m.media-amazon.com/images/M/MV5BZmY0MzBlNjctNTRmNy00Njk3LWFjMzctMWQwZDAwMGJmY2MyXkEyXkFqcGdeQXVyMDM2NDM2MQ@@._V1_.jpg',
                    },
                ]
            },
            {
                'title': 'Peaky Blinders',
                'description': 'A gangster family epic set in 1900s England, centering on a gang who sew razor blades in the peaks of their caps, and their fierce boss Tommy Shelby.',
                'cast': 'Cillian Murphy, Paul Anderson, Sophie Rundle',
                'video_url': 'https://ok.ru/videoembed/2289155315326',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BMThlOWE3MWEtZjM4Ny00M2FiLTkyMmYtZGY3ZTcyMzM5YmNlXkEyXkFqcGdeQXVyMTEyMjM2NDc2._V1_.jpg',
                'content_type': 'series',
                'is_popular': True,
                'genres': ['Crime', 'Drama'],
                'episodes': [
                    {
                        'title': 'Episode 1',
                        'season_number': 1,
                        'episode_number': 1,
                        'description': 'Thomas Shelby and his family run the most feared and powerful local gang, the Peaky Blinders. Named for their practice of sewing razor blades into the peaks of their caps, they make money from illegal betting, protection and the black market.',
                        'video_url': 'https://ok.ru/videoembed/2289155315326',
                        'poster_url': 'https://m.media-amazon.com/images/M/MV5BMThlOWE3MWEtZjM4Ny00M2FiLTkyMmYtZGY3ZTcyMzM5YmNlXkEyXkFqcGdeQXVyMTEyMjM2NDc2._V1_.jpg',
                    },
                    {
                        'title': 'Episode 2',
                        'season_number': 1,
                        'episode_number': 2,
                        'description': 'Thomas fixes a horse race, provoking the ire of local kingpin Billy Kimber. He also starts a war with gypsy family the Lees. Meanwhile, Inspector Campbell carries out a vicious raid of Small Heath in search of the stolen guns.',
                        'video_url': 'https://ok.ru/videoembed/2289155315326',
                        'poster_url': 'https://m.media-amazon.com/images/M/MV5BMThlOWE3MWEtZjM4Ny00M2FiLTkyMmYtZGY3ZTcyMzM5YmNlXkEyXkFqcGdeQXVyMTEyMjM2NDc2._V1_.jpg',
                    },
                ]
            },
            {
                'title': 'The Queen\'s Gambit',
                'description': 'Orphaned at the tender age of nine, prodigious introvert Beth Harmon discovers and masters the game of chess in 1960s USA. But child stardom comes at a price.',
                'cast': 'Anya Taylor-Joy, Chloe Pirrie, Bill Camp',
                'video_url': 'https://ok.ru/videoembed/2289155315326',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BM2EwMmRhMmUtMzBmMS00ZDQ3LTg4OGEtNjlkODk3ZTMxMmJlXkEyXkFqcGdeQXVyMjM5ODk1NDU@._V1_.jpg',
                'content_type': 'series',
                'is_new_release': True,
                'genres': ['Drama'],
                'episodes': [
                    {
                        'title': 'Openings',
                        'season_number': 1,
                        'episode_number': 1,
                        'description': 'Sent to an orphanage at age 9, Beth develops an uncanny knack for chess and a growing dependence on the green tranquilizers given to the children.',
                        'video_url': 'https://ok.ru/videoembed/2289155315326',
                        'poster_url': 'https://m.media-amazon.com/images/M/MV5BM2EwMmRhMmUtMzBmMS00ZDQ3LTg4OGEtNjlkODk3ZTMxMmJlXkEyXkFqcGdeQXVyMjM5ODk1NDU@._V1_.jpg',
                    },
                    {
                        'title': 'Exchanges',
                        'season_number': 1,
                        'episode_number': 2,
                        'description': 'Nine years later, a teenage Beth is adjusting to suburban life with her adoptive mother when a family friend introduces her to a local chess tournament.',
                        'video_url': 'https://ok.ru/videoembed/2289155315326',
                        'poster_url': 'https://m.media-amazon.com/images/M/MV5BM2EwMmRhMmUtMzBmMS00ZDQ3LTg4OGEtNjlkODk3ZTMxMmJlXkEyXkFqcGdeQXVyMjM5ODk1NDU@._V1_.jpg',
                    },
                ]
            },
            {
                'title': 'Squid Game',
                'description': 'Hundreds of cash-strapped players accept a strange invitation to compete in children\'s games. Inside, a tempting prize awaits with deadly high stakes: a survival game that has a whopping 45.6 billion-won prize at stake.',
                'cast': 'Lee Jung-jae, Park Hae-soo, Wi Ha-jun',
                'video_url': 'https://ok.ru/videoembed/2289155315326',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BYWE3MDVkN2EtNjQ5MS00ZDQ4LTliNzYtMjc2YWMzMDEwMTA3XkEyXkFqcGdeQXVyMTEzMTI1Mjk3._V1_.jpg',
                'content_type': 'series',
                'is_new_release': True,
                'genres': ['Action', 'Drama', 'Mystery'],
                'episodes': [
                    {
                        'title': 'Red Light, Green Light',
                        'season_number': 1,
                        'episode_number': 1,
                        'description': 'Hoping to win easy money, a broke and desperate Gi-hun agrees to take part in an enigmatic game. Not long into the first round, unforeseen horrors unfold.',
                        'video_url': 'https://ok.ru/videoembed/2289155315326',
                        'poster_url': 'https://m.media-amazon.com/images/M/MV5BYWE3MDVkN2EtNjQ5MS00ZDQ4LTliNzYtMjc2YWMzMDEwMTA3XkEyXkFqcGdeQXVyMTEzMTI1Mjk3._V1_.jpg',
                    },
                    {
                        'title': 'Hell',
                        'season_number': 1,
                        'episode_number': 2,
                        'description': 'Split on whether to continue or quit, the group holds a vote. But their realities in the outside world may prove to be just as unforgiving as the game.',
                        'video_url': 'https://ok.ru/videoembed/2289155315326',
                        'poster_url': 'https://m.media-amazon.com/images/M/MV5BYWE3MDVkN2EtNjQ5MS00ZDQ4LTliNzYtMjc2YWMzMDEwMTA3XkEyXkFqcGdeQXVyMTEzMTI1Mjk3._V1_.jpg',
                    },
                ]
            },
            {
                'title': 'Loki',
                'description': 'The mercurial villain Loki resumes his role as the God of Mischief in a new series that takes place after the events of "Avengers: Endgame."',
                'cast': 'Tom Hiddleston, Owen Wilson, Gugu Mbatha-Raw',
                'video_url': 'https://ok.ru/videoembed/2289155315326',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BNTkwOTE1ZDYtODQ3Yy00YTYwLTg0YWQtYmVkNmFjNGZlYmRiXkEyXkFqcGdeQXVyNTc4MjczMTM@._V1_.jpg',
                'content_type': 'series',
                'is_new_release': True,
                'genres': ['Action', 'Adventure', 'Fantasy'],
                'episodes': [
                    {
                        'title': 'Glorious Purpose',
                        'season_number': 1,
                        'episode_number': 1,
                        'description': 'After stealing the Tesseract in "Avengers: Endgame," Loki lands before the Time Variance Authority.',
                        'video_url': 'https://ok.ru/videoembed/2289155315326',
                        'poster_url': 'https://m.media-amazon.com/images/M/MV5BNTkwOTE1ZDYtODQ3Yy00YTYwLTg0YWQtYmVkNmFjNGZlYmRiXkEyXkFqcGdeQXVyNTc4MjczMTM@._V1_.jpg',
                    },
                    {
                        'title': 'The Variant',
                        'season_number': 1,
                        'episode_number': 2,
                        'description': 'Mobius puts Loki to work, but not everyone at TVA is thrilled about the God of Mischief\'s presence.',
                        'video_url': 'https://ok.ru/videoembed/2289155315326',
                        'poster_url': 'https://m.media-amazon.com/images/M/MV5BNTkwOTE1ZDYtODQ3Yy00YTYwLTg0YWQtYmVkNmFjNGZlYmRiXkEyXkFqcGdeQXVyNTc4MjczMTM@._V1_.jpg',
                    },
                ]
            },
            {
                'title': 'WandaVision',
                'description': 'Blends the style of classic sitcoms with the MCU, in which Wanda Maximoff and Vision - two super-powered beings living their ideal suburban lives - begin to suspect that everything is not as it seems.',
                'cast': 'Elizabeth Olsen, Paul Bettany, Kathryn Hahn',
                'video_url': 'https://ok.ru/videoembed/2289155315326',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BYjJiZmE5ZDgtYWUxZi00MWI1LTg2MmEtZmUwZGE2YzRkNTE5XkEyXkFqcGdeQXVyMTkxNjUyNQ@@._V1_.jpg',
                'content_type': 'series',
                'is_new_release': True,
                'genres': ['Action', 'Comedy', 'Drama'],
                'episodes': [
                    {
                        'title': 'Filmed Before a Live Studio Audience',
                        'season_number': 1,
                        'episode_number': 1,
                        'description': 'Wanda and Vision struggle to conceal their powers during dinner with Vision\'s boss and his wife.',
                        'video_url': 'https://ok.ru/videoembed/2289155315326',
                        'poster_url': 'https://m.media-amazon.com/images/M/MV5BYjJiZmE5ZDgtYWUxZi00MWI1LTg2MmEtZmUwZGE2YzRkNTE5XkEyXkFqcGdeQXVyMTkxNjUyNQ@@._V1_.jpg',
                    },
                    {
                        'title': 'Don\'t Touch That Dial',
                        'season_number': 1,
                        'episode_number': 2,
                        'description': 'Wanda and Vision put on a magic show in their community talent show, while trying to conceal their powers from their neighbors.',
                        'video_url': 'https://ok.ru/videoembed/2289155315326',
                        'poster_url': 'https://m.media-amazon.com/images/M/MV5BYjJiZmE5ZDgtYWUxZi00MWI1LTg2MmEtZmUwZGE2YzRkNTE5XkEyXkFqcGdeQXVyMTkxNjUyNQ@@._V1_.jpg',
                    },
                ]
            },
            {
                'title': 'The Falcon and the Winter Soldier',
                'description': 'Following the events of "Avengers: Endgame," Sam Wilson and Bucky Barnes team up in a global adventure that tests their abilities and their patience.',
                'cast': 'Anthony Mackie, Sebastian Stan, Wyatt Russell',
                'video_url': 'https://ok.ru/videoembed/2289155315326',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BODNiODVmYjItM2MyMC00ZWQyLTgyMGYtNzJjMmVmZTY2OTczXkEyXkFqcGdeQXVyNzk3NDUzNTc@._V1_.jpg',
                'content_type': 'series',
                'is_new_release': True,
                'genres': ['Action', 'Adventure', 'Drama'],
                'episodes': [
                    {
                        'title': 'New World Order',
                        'season_number': 1,
                        'episode_number': 1,
                        'description': 'Sam Wilson and Bucky Barnes realize that their futures are anything but normal.',
                        'video_url': 'https://ok.ru/videoembed/2289155315326',
                        'poster_url': 'https://m.media-amazon.com/images/M/MV5BODNiODVmYjItM2MyMC00ZWQyLTgyMGYtNzJjMmVmZTY2OTczXkEyXkFqcGdeQXVyNzk3NDUzNTc@._V1_.jpg',
                    },
                    {
                        'title': 'The Star-Spangled Man',
                        'season_number': 1,
                        'episode_number': 2,
                        'description': 'John Walker is named Captain America, and Sam and Bucky team up against the rebel group.',
                        'video_url': 'https://ok.ru/videoembed/2289155315326',
                        'poster_url': 'https://m.media-amazon.com/images/M/MV5BODNiODVmYjItM2MyMC00ZWQyLTgyMGYtNzJjMmVmZTY2OTczXkEyXkFqcGdeQXVyNzk3NDUzNTc@._V1_.jpg',
                    },
                ]
            },
            {
                'title': 'Arcane',
                'description': 'Set in utopian Piltover and the oppressed underground of Zaun, the story follows the origins of two iconic League champions-and the power that will tear them apart.',
                'cast': 'Hailee Steinfeld, Ella Purnell, Kevin Alejandro',
                'video_url': 'https://ok.ru/videoembed/2289155315326',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BYmU5OWM5ZTAtNjUzOC00NmUyLTgyOWMtMjlkNjdlMDAzMzU1XkEyXkFqcGdeQXVyMDM2NDM2MQ@@._V1_.jpg',
                'content_type': 'series',
                'is_new_release': True,
                'genres': ['Animation', 'Action', 'Adventure'],
                'episodes': [
                    {
                        'title': 'Welcome to the Playground',
                        'season_number': 1,
                        'episode_number': 1,
                        'description': 'Orphaned sisters Vi and Powder bring trouble to Zaun\'s underground streets in the wake of a heist in posh Piltover.',
                        'video_url': 'https://ok.ru/videoembed/2289155315326',
                        'poster_url': 'https://m.media-amazon.com/images/M/MV5BYmU5OWM5ZTAtNjUzOC00NmUyLTgyOWMtMjlkNjdlMDAzMzU1XkEyXkFqcGdeQXVyMDM2NDM2MQ@@._V1_.jpg',
                    },
                    {
                        'title': 'Some Mysteries Are Better Left Unsolved',
                        'season_number': 1,
                        'episode_number': 2,
                        'description': 'Idealistic inventor Jayce attempts to harness magic through science — despite his mentor\'s warnings. Criminal kingpin Silco tests a powerful substance.',
                        'video_url': 'https://ok.ru/videoembed/2289155315326',
                        'poster_url': 'https://m.media-amazon.com/images/M/MV5BYmU5OWM5ZTAtNjUzOC00NmUyLTgyOWMtMjlkNjdlMDAzMzU1XkEyXkFqcGdeQXVyMDM2NDM2MQ@@._V1_.jpg',
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

            # Create movie
            movie_data['poster'] = "https://m.media-amazon.com/images/M/MV5BYmU5OWM5ZTAtNjUzOC00NmUyLTgyOWMtMjlkNjdlMDAzMzU1XkEyXkFqcGdeQXVyMDM2NDM2MQ@@._V1_.jpg"
            movie, created = Video.objects.get_or_create(
                slug=slug,
                defaults={**movie_data}
            )

            # Add genres
            movie.genres.set(movie_genres)

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
