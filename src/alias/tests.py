from django.test import TestCase

from alias.models import Alias, get_aliases, alias_replace
import datetime
import pytz


class TestModelTest(TestCase):

    def setUp(self):

        '''alias1_target1_first_range'''
        Alias.objects.create(
            alias='alias1', target='target1',
            start=datetime.datetime(2020, 1, 1, 16, 28, 36, 123456, tzinfo=pytz.UTC),
            end=datetime.datetime(2020, 2, 1, 16, 28, 36, 123456, tzinfo=pytz.UTC)
        )

        '''alias1_target1_second_range'''
        Alias.objects.create(
            alias='alias1', target='target1',
            start=datetime.datetime(2020, 5, 1, 16, 28, 36, 123456, tzinfo=pytz.UTC),
            end=datetime.datetime(2020, 6, 1, 16, 28, 36, 123456, tzinfo=pytz.UTC)
        )

        '''alias2_target1_overlap_range'''
        Alias.objects.create(
            alias='alias2', target='target1',
            start=datetime.datetime(2020, 1, 1, 16, 28, 36, 123456, tzinfo=pytz.UTC),
            end=datetime.datetime(2020, 2, 1, 16, 28, 36, 123456, tzinfo=pytz.UTC)
        )

        '''alias2_target2_endless_range'''
        Alias.objects.create(
            alias='alias2', target='target2',
            start=datetime.datetime(2021, 1, 1, 16, 28, 36, 123456, tzinfo=pytz.UTC),
            end=None
        )

    def test_alias_count(self):
        count = Alias.objects.count()
        self.assertEqual(count, 4)

    def test_create_alias_negative(self):

        """
        new_alias = alias1_target1_first_range = Alias.objects.create(
            alias='alias1', target='target1',
            start=datetime.datetime(2020, 1, 1, 16, 28, 36, 123456, tzinfo=pytz.UTC),
            end=datetime.datetime(2020, 2, 1, 16, 28, 36, 123456, tzinfo=pytz.UTC)
        )
        """

        with self.assertRaises(Exception) as context:
            Alias.objects.create(
                alias='alias1', target='target1',
                start=datetime.datetime(2020, 1, 1, 16, 28, 36, 123456, tzinfo=pytz.UTC),
                end=datetime.datetime(2020, 2, 1, 16, 28, 36, 123456, tzinfo=pytz.UTC)
            )
        # print(context.exception, type(context.exception))
        self.assertTrue('Such an Object already exists !!!' in str(context.exception))

        count = Alias.objects.count()
        self.assertEqual(count, 4)

    def test_create_alias_positive(self):

        """alias1_target1_second_range"""

        new_alias = Alias.objects.create(
            alias='alias1', target='target1',
            start=datetime.datetime(2020, 3, 1, 16, 28, 36, 123456, tzinfo=pytz.UTC),
            end=datetime.datetime(2020, 4, 1, 16, 28, 36, 123456, tzinfo=pytz.UTC)
        )
        qs = Alias.objects.filter(
            alias=new_alias.alias,
            target=new_alias.target,
            start=new_alias.start,
            end=new_alias.end)
        # print(qs , type(qs), len(qs), qs[0])
        self.assertEqual(new_alias, qs[0])

        count = Alias.objects.count()
        self.assertEqual(count, 5)

    def test_create_alias_microsecond_interval_positive(self):

        """alias1_target1_second_range"""

        new_alias = Alias.objects.create(
            alias='alias1', target='target1',
            start=datetime.datetime(2020, 2, 1, 16, 28, 36, 123456, tzinfo=pytz.UTC),
            end=datetime.datetime(2020, 4, 1, 16, 28, 36, 123456, tzinfo=pytz.UTC)
        )
        qs = Alias.objects.filter(
            alias=new_alias.alias,
            target=new_alias.target,
            start=new_alias.start,
            end=new_alias.end)
        # print(qs , type(qs), len(qs), qs[0])
        self.assertEqual(new_alias, qs[0])

        count = Alias.objects.count()
        self.assertEqual(count, 5)

    def test_create_alias_microsecond_interval_negative(self):

        """
        new_alias = alias1_target1_overlap_range = Alias.objects.create(
            alias='alias1', target='target1',
            start=datetime.datetime(2020, 2, 1, 16, 28, 36, 123455, tzinfo=pytz.UTC),
            end=datetime.datetime(2020, 3, 1, 16, 28, 36, 123456, tzinfo=pytz.UTC)
        )
        """

        with self.assertRaises(Exception) as context:
            Alias.objects.create(
                alias='alias1', target='target1',
                start=datetime.datetime(2020, 2, 1, 16, 28, 36, 123455, tzinfo=pytz.UTC),
                end=datetime.datetime(2020, 3, 1, 16, 28, 36, 123456, tzinfo=pytz.UTC)
            )
        # print(context.exception, type(context.exception))
        self.assertTrue('OVERLAPPING Date Range of Objects !' in str(context.exception))

        count = Alias.objects.count()
        self.assertEqual(count, 4)

    def test_get_aliases(self):
        new_alias_1 = Alias.objects.create(
            alias='alias1', target='target1',
            start=datetime.datetime(2020, 2, 1, 16, 28, 36, 123456, tzinfo=pytz.UTC),
            end=datetime.datetime(2020, 4, 1, 16, 28, 36, 123456, tzinfo=pytz.UTC)
        )
        new_alias_2 = Alias.objects.create(
            alias='alias2', target='target1',
            start=datetime.datetime(2020, 2, 1, 16, 28, 36, 123456, tzinfo=pytz.UTC),
            end=datetime.datetime(2020, 4, 1, 16, 28, 36, 123456, tzinfo=pytz.UTC)
        )
        new_alias_3 = Alias.objects.create(
            alias='alias3', target='target1',
            start=datetime.datetime(2020, 2, 1, 16, 28, 36, 123456, tzinfo=pytz.UTC),
            end=datetime.datetime(2020, 4, 1, 16, 28, 36, 123456, tzinfo=pytz.UTC)
        )
        result = get_aliases(
            target='target1',
            point_1=datetime.datetime(2020, 2, 10, 16, 28, 36, 123456, tzinfo=pytz.UTC),
            point_2=datetime.datetime(2020, 3, 10, 16, 28, 36, 123456, tzinfo=pytz.UTC)
        )
        # print(result)
        # expected = {'alias1', 'alias2', 'alias3'}
        expected = {new_alias_3.alias, new_alias_2.alias, new_alias_1.alias}
        self.assertEqual(expected, result)

        count = Alias.objects.count()
        self.assertEqual(count, 7)

    def test_alias_replace_1(self):

        existing_alias = Alias.objects.get(id=4)
        replace_at = datetime.datetime(2021, 2, 1, 16, 28, 36, 123456, tzinfo=pytz.UTC)
        new_alias_value = 'new_alias'

        self.assertEqual(existing_alias.end, None)

        alias_replace(
            existing_alias=existing_alias,
            replace_at=replace_at,
            new_alias_value=new_alias_value)

        self.assertEqual(existing_alias.end, replace_at)

        count = Alias.objects.count()
        self.assertEqual(count, 5)

    def test_alias_replace_2(self):
        existing_alias = Alias.objects.get(id=4)
        replace_at = datetime.datetime(2021, 2, 1, 16, 28, 36, 123456, tzinfo=pytz.UTC)
        new_alias_value = 'new_alias'

        alias_replace(
            existing_alias=existing_alias,
            replace_at=replace_at,
            new_alias_value=new_alias_value)

        count = Alias.objects.count()
        self.assertEqual(count, 5)

        target = existing_alias.target
        expected = Alias.objects.filter(
            alias=new_alias_value,
            target=target,
            start=replace_at,
            end=None
        )
        self.assertEqual(len(expected), 1)
