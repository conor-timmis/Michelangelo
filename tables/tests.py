from django.test import TestCase
from django.contrib.auth.models import User
from .models import Booking, Review
import datetime


class ReviewModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a user
        cls.user = User.objects.create_user(
            'testuser', 'test@example.com', 'testpassword'
        )

        # Create a booking
        cls.booking = Booking.objects.create(
            user=cls.user,
            special_occasion='Bday',
            meal_day=datetime.date.today(),
            meal_time=datetime.time(13, 30),
            number_of_guests=2,
            customer_name='Test User'
        )

        # Create a review
        cls.review = Review.objects.create(
            user=cls.user,
            booking=cls.booking,
            rating=3,
            comment='Good service!'
        )

    def test_review_creation(self):
        # Check if the review was created with the correct details
        self.assertEqual(self.review.user.username, 'testuser')
        self.assertEqual(self.review.booking, self.booking)
        self.assertEqual(self.review.rating, 3)
        self.assertEqual(self.review.comment, 'Good service!')

    def test_invalid_rating(self):
        # Create a review with an invalid rating and
        # check if it raises an exception
        with self.assertRaises(Exception):
            Review.objects.create(
                user=self.user,
                booking=self.booking,
                rating=6,
                comment='Good service!'
            ).full_clean()
