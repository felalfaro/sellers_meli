from data import get_categories, get_tipo_pago_pais


def main():
    chile = 'MLC'
    data = get_categories()
    print(data[data['country'] == chile])


if __name__ == '__main__':
    main()
