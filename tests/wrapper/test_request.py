from unittest import TestCase

from bb_wrapper.wrapper.request import RequestsWrapper


class RequestsWrapperTestCase(TestCase):
    maxDiff = None

    def test_contruct_url_1(self):
        """
        Dado:
            - uma base_url 'http://foo.bar'
            - um wrapper RequestsWrapper(self.base_url)
        Quando:
            - self.wrapper._construct_url('acao1', 'id1', 'subacao2', 'id2')
        Então:
            - o resultado deve ser "http://foo.bar/acao1/id1/subacao2/id2/"
        """
        base_url = 'http://foo.bar'
        wrapper = RequestsWrapper(base_url)

        result = wrapper._construct_url('acao1', 'id1', 'subacao2', 'id2')

        expected = "http://foo.bar/acao1/id1/subacao2/id2/"

        self.assertEqual(result, expected)

    def test_contruct_url_2(self):
        """
        Dado:
            - uma base_url 'http://foo.bar/'
            - um wrapper RequestsWrapper(self.base_url)
        Quando:
            - self.wrapper._construct_url('acao1', 'id1', 'subacao2', 'id2')
        Então:
            - o resultado deve ser "http://foo.bar/acao1/id1/subacao2/id2/"
        """
        base_url = 'http://foo.bar/'
        wrapper = RequestsWrapper(base_url)

        result = wrapper._construct_url('acao1', 'id1', 'subacao2', 'id2')

        expected = "http://foo.bar/acao1/id1/subacao2/id2/"

        self.assertEqual(result, expected)

    def test_contruct_url_3(self):
        """
        Dado:
            - uma base_url 'http://foo.bar'
            - um wrapper RequestsWrapper(self.base_url)
        Quando:
            - self.wrapper._construct_url('acao1', 'id1', 'subacao2', 'id2', search='query1=1&query2=2')
        Então:
            - o resultado deve ser "http://foo.bar/acao1/id1/subacao2/id2/?query1=1&query2=2"
        """
        base_url = 'http://foo.bar'
        wrapper = RequestsWrapper(base_url)

        result = wrapper._construct_url('acao1', 'id1', 'subacao2', 'id2', search='query1=1&query2=2')

        expected = "http://foo.bar/acao1/id1/subacao2/id2/?query1=1&query2=2"

        self.assertEqual(result, expected)

    def test_contruct_url_4(self):
        """
        Dado:
            - uma base_url 'http://foo.bar'
            - um wrapper RequestsWrapper(self.base_url)
        Quando:
            - self.wrapper._construct_url('acao1', 'id1', 'subacao2', 'id2', search=dict(query1=1, query2=2))
        Então:
            - o resultado deve ser "http://foo.bar/acao1/id1/subacao2/id2/?query1=1&query2=2"
        """
        base_url = 'http://foo.bar'
        wrapper = RequestsWrapper(base_url)

        result = wrapper._construct_url('acao1', 'id1', 'subacao2', 'id2', search=dict(query1=1, query2=2))

        expected = "http://foo.bar/acao1/id1/subacao2/id2/?query1=1&query2=2"

        self.assertEqual(result, expected)
