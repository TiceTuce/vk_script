from vk_api import VkApi
import os
from date_convert import convert_to_unix


def get_posts_by_date(vk, group_id):
    date = input("Please input start date format yyyy.mm.dd: ")
    unix = convert_to_unix(date)

    offset = 0
    posts_array = []
    flag = True
    while flag:
        wall = vk.wall.get(owner_id=group_id, count=100, offset=offset)['items']
        if wall[-1]['date'] > unix:
            posts_array.extend(wall)
        else:
            for post in wall:
                if post['date'] < unix:
                    flag = False
                    break
                posts_array.append(post)
        offset += 100

    return posts_array


def sort_posts(posts_array: list, field: str, ascending=True):
    return sorted(posts_array, key=lambda x: x[field]['count'], reverse=ascending)


def print_posts_links(data_array, domain, group_id, count=10):
    data_array = data_array[:count]
    group_wall_url = f"https://vk.com/{domain}?w=wall{group_id}_"
    for post in data_array:
        post_id = post['id']
        post_url = group_wall_url + str(post_id)
        print(post_url)


def main():
    # Authorize
    token = os.getenv("token")
    vk_session = VkApi(token=token)
    vk = vk_session.get_api()

    # Get posts info from KHTI public
    domain = "khti_sfu"
    group_id = str(-vk.groups.getById(group_id=domain)[0]['id'])
    posts_array = get_posts_by_date(vk, group_id)
    sorted_posts = sort_posts(posts_array, 'reposts')

    # Print posts links in terminal
    print_posts_links(sorted_posts, domain, group_id)


if __name__ == "__main__":
    main()
