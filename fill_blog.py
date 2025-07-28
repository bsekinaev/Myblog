import os
import sys
import django
import random
from faker import Faker
from datetime import timedelta

# Расчёт пути к корню проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Установка настроек Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myblog.settings")

# Проверка путей перед инициализацией
print(f"BASE_DIR: {BASE_DIR}")
print(f"Python path: {sys.path}")

django.setup()

from django.contrib.auth.models import User
from django.utils import timezone
from blog.models import Post, Comment, Like, Tag

def create_test_data():
    fake = Faker()

    # Создаем суперпользователя
    if not User.objects.filter(username='admin').exists():
        admin = User.objects.create_superuser('admin', 'admin@example.com', 'admin')
        admin.save()
        print('Создан суперпользователь: admin')

    # Создаем обычных пользователей
    users = []
    for i in range(1, 6):
        username = f'user{i}'
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(
                username=username,
                email=f'{username}@example.com',
                password='testpassword123'
            )
            users.append(user)
            print(f'Создан пользователь: {username}')
        else:
            users.append(User.objects.get(username=username))

    # Создаем теги
    tags = []
    tag_names = ['Django', 'Python', 'Web', 'Development', 'Programming', 'Tutorial', 'Tips', 'Frontend', 'Backend', 'Database']
    for name in tag_names:
        tag, created = Tag.objects.get_or_create(name=name)
        tags.append(tag)
        if created:
            print(f'Создан тег: {name}')

    # Создаем посты
    for i in range(50):
        title = fake.sentence(nb_words=6)
        content = "\n\n".join(fake.paragraphs(nb=3))
        author = random.choice(users)
        random_days = random.randint(0, 365)
        post_date = timezone.now() - timedelta(days=random_days)

        post = Post.objects.create(
            title=title,
            content=content,
            author=author,
            date_posted=post_date
        )

        # Добавляем теги к посту
        post_tags = random.sample(tags, k=random.randint(1, 3))
        post.tags.set(post_tags)

        print(f'Создан пост: "{title}" от {author.username}')

        # Создаем комментарии для поста
        for j in range(random.randint(0, 10)):
            comment_author = random.choice(users)
            comment_date = post_date + timedelta(days=random.randint(0, 30))
            Comment.objects.create(
                post=post,
                author=comment_author,
                content=fake.paragraph(),
                created_at=comment_date
            )

        # Создаем лайки для поста
        likers = random.sample(users, k=random.randint(0, len(users)))
        for liker in likers:
            like_date = post_date + timedelta(days=random.randint(0, 30))
            Like.objects.get_or_create(
                user=liker,
                post=post,
                defaults={'created_at': like_date}
            )

if __name__ == '__main__':
    print("Начинаем наполнение блога тестовыми данными...")
    create_test_data()
    print("Готово! Блог наполнен тестовыми данными.")