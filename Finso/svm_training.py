import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import joblib

categories = {
    'entertainment': ['happy', 'restaurant', 'food', 'kitchen', 'hotel', 'room', 'park', 'movie', 'cinema', 'popcorn', 'combo meal'],
    'home_utility': ['internet', 'telephone', 'electricity', 'meter', 'wifi', 'broadband', 'consumer', 'reading', 'gas', 'water', 'postpaid', 'prepaid'],
    'grocery': ['bigbasket', 'milk', 'atta', 'sugar', 'sunflower oil', 'bread', 'vegetable', 'fruit', 'salt', 'paneer', 'brinjal', 'tomato', 'potato'],
    'investment': ['endowment', 'grant', 'loan', 'applicant', 'income', 'expenditure', 'profit', 'interest', 'expense', 'finance', 'property', 'money', 'fixed deposit', 'kissan', 'vikas'],
    'transport': ['car', 'cab', 'ola', 'uber', 'autorickshaw', 'railway', 'air', 'emirates', 'aerofloat', 'taxi', 'booking', 'road', 'highway'],
    'shopping': ['dress', 'iphone', 'laptop', 'saree', 'max', 'pantaloons', 'westside', 'vedic', 'makeup', 'lipstick', 'cosmetics', 'mac', 'facewash', 'heels', 'crocs', 'footwear', 'purse', 'hair', 'ribbons'],
    'education': ['pencil', 'pen', 'geometry box', 'ink', 'pages', 'book', 'books', 'notebook', 'textbook'],
    'healthcare': ['medicine', 'hospital', 'doctor', 'pharmacy', 'medical', 'consultation', 'insurance', 'dentist', 'vaccination', 'surgery', 'treatment'],
    'utilities': ['cable', 'subscription', 'Netflix', 'Amazon Prime', 'Hulu', 'Spotify', 'electricity bill', 'water bill', 'gas bill', 'internet bill'],
    'personal_care': ['shampoo', 'conditioner', 'soap', 'lotion', 'deodorant', 'toothpaste', 'razor', 'skincare', 'haircare', 'fragrance', 'cosmetics'],
    'dining_out': ['fast food', 'restaurant', 'cafe', 'coffee', 'pizza', 'burger', 'sushi', 'fine dining', 'bar', 'pub', 'cocktail', 'dessert'],
    'travel': ['flight', 'hotel', 'rental car', 'train', 'bus', 'taxi', 'fuel', 'toll', 'parking', 'luggage', 'passport', 'visa', 'travel insurance'],
    'clothing': ['shirt', 'jeans', 'dress', 'shoes', 'accessories', 'underwear', 'socks', 'jacket', 'coat', 'hat', 'scarf', 'gloves', 'activewear'],
    'electronics': ['smartphone', 'laptop', 'tablet', 'TV', 'camera', 'headphones', 'speakers', 'charger', 'cables', 'smartwatch', 'gaming console'],
    'home_improvement': ['furniture', 'appliances', 'paint', 'tools', 'hardware', 'decor', 'lighting', 'flooring', 'renovation', 'landscaping', 'gardening'],
    'subscriptions': ['magazine', 'newspaper', 'streaming service', 'gym membership', 'software', 'cloud storage', 'meal kit', 'wine club', 'beauty box'],
    'gifts': ['birthday', 'anniversary', 'wedding', 'baby shower', 'holiday', 'Christmas', "Valentine's Day", "Mother's Day", "Father's Day", 'graduation'],
    'pet_care': ['food', 'treats', 'toys', 'grooming', 'vet', 'medication', 'boarding', 'pet insurance', 'litter', 'leash', 'collar', 'bed'],
    'car_maintenance': ['gas', 'oil change', 'car wash', 'tire rotation', 'repairs', 'maintenance', 'registration', 'insurance', 'parking fees', 'tolls'],
    'kids': ['diapers', 'formula', 'baby food', 'clothing', 'toys', 'books', 'school supplies', 'activities', 'daycare', 'education expenses'],
    'entertainment_outdoor': ['tickets', 'festivals', 'concerts', 'amusement parks', 'zoos', 'museums', 'sporting events', 'camping', 'hiking', 'picnics'],
    'hobbies': ['crafting supplies', 'art supplies', 'musical instruments', 'lessons', 'classes', 'hobby-related equipment', 'materials'],
    'taxes': ['income tax', 'property tax', 'sales tax', 'excise tax', 'vehicle tax', 'business tax', 'tax preparation fees', 'accountant fees'],
    'insurance': ['health insurance', 'life insurance', 'car insurance', 'home insurance', 'renters insurance', 'travel insurance', 'pet insurance'],
    'bank_fees': ['ATM fees', 'overdraft fees', 'wire transfer fees', 'foreign transaction fees', 'account maintenance fees', 'late payment fees'],
    'utilities_home': ['garbage collection', 'sewage', 'recycling', 'pest control', 'maintenance fees', 'home security', 'alarm system'],
    'personal_development': ['courses', 'workshops', 'seminars', 'coaching', 'self-help books', 'meditation apps', 'therapy', 'retreats'],
    'charity': ['donations', 'fundraising events', 'sponsorships', 'volunteer expenses', 'charitable gifts', 'NGO contributions'],
    'financial_services': ['financial advisor fees', 'investment management fees', 'brokerage fees', 'banking fees', 'loan interest'],
    'sports': ['gym membership', 'equipment', 'apparel', 'team fees', 'event tickets', 'classes', 'coaching', 'sports gear maintenance'],
    'beauty_services': ['salon', 'spa', 'haircut', 'coloring', 'manicure', 'pedicure', 'waxing', 'facials', 'massages', 'beauty treatments'],
    'office_supplies': ['paper', 'pens', 'printer ink', 'envelopes', 'stamps', 'folders', 'binders', 'tape', 'staples', 'desk accessories'],
    'repairs_maintenance': ['home repairs', 'appliance repairs', 'car repairs', 'maintenance services', 'handyman services'],
    'home_cleaning': ['cleaning supplies', 'maid service', 'vacuum cleaner', 'mop', 'broom', 'cleaning solutions', 'laundry detergent'],
    'eating_in': ['groceries', 'meal ingredients', 'cooking supplies', 'meal prep services', 'delivery fees', 'kitchenware'],
    'entertainment_indoor': ['board games', 'puzzles', 'video games', 'streaming services', 'movie rentals', 'home theater equipment'],
    'health_wellness': ['gym membership', 'fitness classes', 'yoga classes', 'meditation apps', 'supplements', 'wellness retreats'],
    'travel_local': ['gas', 'public transportation', 'parking fees', 'tolls', 'day trips', 'local attractions', 'guided tours'],
    'gardening': ['seeds', 'plants', 'tools', 'fertilizer', 'soil', 'pots', 'watering cans', 'gardening gloves', 'outdoor decor'],
    'DIY_projects': ['materials', 'tools', 'equipment rental', 'project guides', 'DIY workshops', 'instructional books'],
    'financial_planning': ['financial advisor fees', 'retirement planning services', 'investment advice', 'financial software'],
    'home_decor': ['furniture', 'decor items', 'artwork', 'rugs', 'curtains', 'bedding', 'pillows', 'throws', 'candles'],
    'home_security': ['alarm system', 'surveillance cameras', 'security service fees', 'locks', 'motion sensors'],
    'photography': ['camera equipment', 'lenses', 'memory cards', 'photo editing software', 'prints', 'frames'],
    'home_office': ['desk', 'chair', 'computer', 'printer', 'office supplies', 'organization tools', 'ergonomic accessories'],
    'home_renovation': ['materials', 'contractor fees', 'permits', 'demolition', 'construction', 'remodeling'],
    'self_care': ['spa treatments', 'massage therapy', 'meditation apps', 'yoga classes', 'wellness retreats'],
    'financial_education': ['books', 'courses', 'seminars', 'workshops', 'online tutorials', 'educational subscriptions'],
    'home_entertainment': ['streaming services', 'DVDs', 'Blu-rays', 'video games', 'board games', 'puzzles', 'home theater equipment'],
    'socializing': ['dining out', 'drinks', 'events', 'parties', 'concerts', 'movies', 'sports games', 'activities']
}


all_keywords = [word.lower() for keywords in categories.values() for word in keywords]

X_train = []
y_train = []
for category, keywords in categories.items():
    for keyword in keywords:
        X_train.append(keyword.lower()) 
        y_train.append(category)

tfidf_vectorizer = TfidfVectorizer(vocabulary=set(all_keywords))
X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)

svm_classifier = SVC(kernel='linear')
svm_classifier.fit(X_train_tfidf, y_train)

joblib.dump(svm_classifier, 'svm_model.pkl')
joblib.dump(tfidf_vectorizer, 'tfidf_vectorizer.pkl')
