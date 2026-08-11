"""
Seed script – run after creating the database and tables.
Usage: python seed.py
"""
from database import SessionLocal, engine, Base
from models import (
    User, Customer, Manager, Destination, Hotel, HotelRoom,
    Trip, TripItinerary, Amenity, ApprovalStatus, UserRole
)
from auth import get_password_hash

Base.metadata.create_all(bind=engine)
db = SessionLocal()


def seed():
    # Admin
    if not db.query(User).filter(User.email == "admin@travel.com").first():
        admin = User(
            full_name="Platform Admin",
            email="admin@travel.com",
            phone="+10000000000",
            hashed_password=get_password_hash("admin123"),
            role=UserRole.admin
        )
        db.add(admin)
        db.commit()
        print("Created admin@travel.com / admin123")

    # Manager
    if not db.query(User).filter(User.email == "manager@travel.com").first():
        mgr_user = User(
            full_name="Hotel Manager",
            email="manager@travel.com",
            phone="+10000000001",
            hashed_password=get_password_hash("manager123"),
            role=UserRole.manager
        )
        db.add(mgr_user)
        db.commit()
        db.refresh(mgr_user)
        manager = Manager(user_id=mgr_user.id, company_name="Wanderlust Hotels")
        db.add(manager)
        db.commit()
        print("Created manager@travel.com / manager123")

    # Customer
    if not db.query(User).filter(User.email == "customer@travel.com").first():
        cust_user = User(
            full_name="John Traveler",
            email="customer@travel.com",
            phone="+10000000002",
            hashed_password=get_password_hash("customer123"),
            role=UserRole.customer
        )
        db.add(cust_user)
        db.commit()
        db.refresh(cust_user)
        db.add(Customer(user_id=cust_user.id, address="123 Explorer St"))
        db.commit()
        print("Created customer@travel.com / customer123")

    manager = db.query(Manager).first()

    # Destinations
    destinations_data = [
        {
            "name": "Bali",
            "country": "Indonesia",
            "description": "Tropical paradise with beaches, temples and rice terraces.",
            "image_url": "https://images.unsplash.com/photo-1537996194471-e657df975ab4?w=800",
            "starting_price": 89.0
        },
        {
            "name": "Paris",
            "country": "France",
            "description": "The city of lights, romance, art and world-class cuisine.",
            "image_url": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=800",
            "starting_price": 120.0
        },
        {
            "name": "Tokyo",
            "country": "Japan",
            "description": "Where ancient temples meet futuristic skyscrapers.",
            "image_url": "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=800",
            "starting_price": 110.0
        },
        {
            "name": "Santorini",
            "country": "Greece",
            "description": "Iconic white-washed buildings and stunning sunsets over the caldera.",
            "image_url": "https://images.unsplash.com/photo-1570077186671-e8dd5b0b4d8b?w=800",
            "starting_price": 150.0
        },
        {
            "name": "New York",
            "country": "USA",
            "description": "The city that never sleeps – Broadway, parks and endless energy.",
            "image_url": "https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?w=800",
            "starting_price": 140.0
        },
    ]

    dest_map = {}
    for d in destinations_data:
        existing = db.query(Destination).filter(Destination.name == d["name"]).first()
        if not existing:
            dest = Destination(**d)
            db.add(dest)
            db.commit()
            db.refresh(dest)
            dest_map[d["name"]] = dest
            print(f"Created destination: {d['name']}")
        else:
            dest_map[d["name"]] = existing

    # Hotels
    hotels_data = [
        {
            "name": "Bali Beach Resort",
            "destination": "Bali",
            "location": "Seminyak, Bali",
            "description": "Luxury beachfront resort with private villas and infinity pools.",
            "star_rating": 5,
            "image_url": "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800",
            "hotel_type": "resort",
            "rooms": [
                {"room_type": "Deluxe Ocean View", "price_per_night": 189.0, "capacity": 2},
                {"room_type": "Garden Villa", "price_per_night": 249.0, "capacity": 3},
                {"room_type": "Presidential Suite", "price_per_night": 499.0, "capacity": 4},
            ]
        },
        {
            "name": "Paris Charm Hotel",
            "destination": "Paris",
            "location": "Le Marais, Paris",
            "description": "Boutique hotel steps away from Notre-Dame and the Seine.",
            "star_rating": 4,
            "image_url": "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800",
            "hotel_type": "boutique",
            "rooms": [
                {"room_type": "Classic Double", "price_per_night": 145.0, "capacity": 2},
                {"room_type": "Superior Suite", "price_per_night": 220.0, "capacity": 2},
            ]
        },
        {
            "name": "Tokyo Sky Tower Hotel",
            "destination": "Tokyo",
            "location": "Shinjuku, Tokyo",
            "description": "Modern high-rise with panoramic city views and rooftop bar.",
            "star_rating": 5,
            "image_url": "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800",
            "hotel_type": "luxury",
            "rooms": [
                {"room_type": "Standard Twin", "price_per_night": 165.0, "capacity": 2},
                {"room_type": "Executive Room", "price_per_night": 210.0, "capacity": 2},
            ]
        },
        {
            "name": "Santorini Cliffside Suites",
            "destination": "Santorini",
            "location": "Oia, Santorini",
            "description": "Cave-style suites carved into the cliff with private plunge pools.",
            "star_rating": 5,
            "image_url": "https://images.unsplash.com/photo-1613395877344-13d4a8e0d49e?w=800",
            "hotel_type": "resort",
            "rooms": [
                {"room_type": "Caldera View Suite", "price_per_night": 320.0, "capacity": 2},
                {"room_type": "Honeymoon Villa", "price_per_night": 450.0, "capacity": 2},
            ]
        },
    ]

    for h in hotels_data:
        if not db.query(Hotel).filter(Hotel.name == h["name"]).first():
            dest = dest_map.get(h["destination"])
            hotel = Hotel(
                name=h["name"],
                location=h["location"],
                description=h["description"],
                star_rating=h["star_rating"],
                image_url=h["image_url"],
                hotel_type=h["hotel_type"],
                destination_id=dest.id if dest else None,
                manager_id=manager.id if manager else None,
                approval_status=ApprovalStatus.approved,
                is_active=True
            )
            db.add(hotel)
            db.commit()
            db.refresh(hotel)
            for r in h["rooms"]:
                room = HotelRoom(hotel_id=hotel.id, **r, available_count=10)
                db.add(room)
            db.commit()
            print(f"Created hotel: {h['name']}")

    # Trips
    trips_data = [
        {
            "title": "Bali Cultural Escape",
            "destination": "Bali",
            "description": "7-day journey through temples, rice terraces, beaches and local villages.",
            "duration_days": 7,
            "price": 899.0,
            "trip_type": "cultural",
            "image_url": "https://images.unsplash.com/photo-1518548419970-58e3b4079ab2?w=800",
            "included": "Hotels, breakfast, guided tours, airport transfers",
            "excluded": "Flights, personal expenses, travel insurance",
            "itinerary": [
                {"day_number": 1, "title": "Arrival & Seminyak", "description": "Airport pickup, beach time and welcome dinner."},
                {"day_number": 2, "title": "Ubud Temples", "description": "Visit Tirta Empul and explore the monkey forest."},
                {"day_number": 3, "title": "Rice Terraces", "description": "Tegalalang terraces and local cooking class."},
            ]
        },
        {
            "title": "Romantic Paris Weekend",
            "destination": "Paris",
            "description": "3-day romantic getaway covering iconic landmarks and Seine cruise.",
            "duration_days": 3,
            "price": 599.0,
            "trip_type": "romantic",
            "image_url": "https://images.unsplash.com/photo-1499856871958-5b9627545d1a?w=800",
            "included": "4-star hotel, breakfast, Seine cruise, Eiffel Tower tickets",
            "excluded": "Flights, lunches & dinners",
            "itinerary": [
                {"day_number": 1, "title": "Arrival & Eiffel Tower", "description": "Check-in and evening Eiffel Tower visit."},
                {"day_number": 2, "title": "Louvre & Seine", "description": "Morning at the Louvre, afternoon river cruise."},
            ]
        },
        {
            "title": "Tokyo Adventure Week",
            "destination": "Tokyo",
            "description": "Explore neon streets, traditional temples, Mt Fuji day trip and street food.",
            "duration_days": 6,
            "price": 1099.0,
            "trip_type": "adventure",
            "image_url": "https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?w=800",
            "included": "Hotels, JR Pass (3 days), guided tours, some meals",
            "excluded": "International flights",
            "itinerary": [
                {"day_number": 1, "title": "Shibuya & Harajuku", "description": "Crossing, shopping and street food."},
                {"day_number": 2, "title": "Asakusa & Skytree", "description": "Senso-ji temple and city views."},
            ]
        },
        {
            "title": "Santorini Sunset Escape",
            "destination": "Santorini",
            "description": "4-day island escape with caldera views, wine tasting and boat trip.",
            "duration_days": 4,
            "price": 799.0,
            "trip_type": "beach",
            "image_url": "https://images.unsplash.com/photo-1613395877344-13d4a8e0d49e?w=800",
            "included": "Cliffside hotel, breakfast, sunset cruise, wine tasting",
            "excluded": "Flights, dinners",
            "itinerary": [
                {"day_number": 1, "title": "Arrival in Oia", "description": "Transfer and sunset at the castle."},
                {"day_number": 2, "title": "Volcano Cruise", "description": "Boat trip to the volcano and hot springs."},
            ]
        },
    ]

    for t in trips_data:
        if not db.query(Trip).filter(Trip.title == t["title"]).first():
            dest = dest_map.get(t["destination"])
            trip = Trip(
                title=t["title"],
                description=t["description"],
                duration_days=t["duration_days"],
                price=t["price"],
                trip_type=t["trip_type"],
                image_url=t["image_url"],
                included=t["included"],
                excluded=t["excluded"],
                destination_id=dest.id if dest else None,
                manager_id=manager.id if manager else None,
                approval_status=ApprovalStatus.approved,
                is_active=True
            )
            db.add(trip)
            db.commit()
            db.refresh(trip)
            for it in t.get("itinerary", []):
                db.add(TripItinerary(trip_id=trip.id, **it))
            db.commit()
            print(f"Created trip: {t['title']}")

    print("\nSeed completed successfully!")
    print("Login credentials:")
    print("  Admin:    admin@travel.com / admin123")
    print("  Manager:  manager@travel.com / manager123")
    print("  Customer: customer@travel.com / customer123")


if __name__ == "__main__":
    try:
        seed()
    finally:
        db.close()
