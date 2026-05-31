# 💇 Salon Scheduler Development

An AI-powered salon appointment scheduling platform that enables customers to discover salons, browse practitioner profiles, analyze reviews, and book appointments through an intelligent scheduling engine.

Built to solve real-world scheduling challenges including practitioner availability, conflict-free bookings, waitlists, cancellations, dynamic scheduling, and smart stylist recommendations.

---

## 🚀 Features

### Customer Booking Experience

* Search salons by location
* Browse real salon data from Google Places API
* View salon ratings, reviews, photos, and business information
* Explore practitioner profiles
* Filter stylists by expertise and ratings
* View real-time availability
* Book appointments instantly
* Reschedule appointments
* Cancel appointments
* Join waitlists for unavailable slots
* Receive booking confirmations and reminders

---

### Intelligent Scheduling Engine

* 30-minute slot generation
* Configurable appointment durations
* Lunch break management
* Off-day scheduling
* Conflict prevention
* Double-booking protection
* Slot reservation during checkout
* Atomic booking transactions
* Real-time availability updates

---

### AI-Powered Features

#### Intelligent Stylist Matching

Recommends practitioners based on:

* Customer preferences
* Booking history
* Stylist expertise
* Ratings and reviews
* Workload balancing
* Availability

---

#### Review Sentiment Analysis

Analyzes customer reviews and extracts:

* Positive feedback
* Negative feedback
* Service quality indicators
* Expertise recognition
* Wait-time complaints

---

#### Smart Waitlist Optimization

Automatically:

* Detects newly available slots
* Matches waitlisted customers
* Prioritizes users
* Sends instant notifications

---

#### Demand Prediction

Analyzes historical booking patterns to:

* Predict peak demand periods
* Identify low-demand slots
* Improve scheduling efficiency
* Support dynamic pricing strategies

---

## 🏗️ System Architecture

```text
┌──────────────────────┐
  Customer Web App     
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
  Next.js Frontend     
└──────────┬───────────┘
           │ REST API
           ▼
┌──────────────────────┐
  NestJS Backend       
└───────┬──────┬───────┘
        │      │
        ▼      ▼
 PostgreSQL   Redis
        │
        ▼
    BullMQ Jobs

External Services
─────────────────
Google Places API
Google Maps
Stripe Sandbox
Twilio SMS
Resend Email
```

---

## Tech Stack

### Frontend

* Next.js 15
* React
* TypeScript
* Tailwind CSS
* ShadCN UI
* React Query
* Zustand

### Backend

* NestJS
* TypeScript
* Prisma ORM
* PostgreSQL
* Redis
* BullMQ

### AI & Analytics

* Sentiment Analysis
* Recommendation Engine
* Demand Prediction
* Scheduling Optimization

### Integrations

* Google Places API
* Google Maps Platform
* Stripe Sandbox
* Twilio
* Resend

### DevOps

* Docker
* Docker Compose
* Nginx
* GitHub Actions

---

## 📂 Project Structure

```bash
Salon-Scheduler-Development/

├── frontend/
│   ├── app/
│   ├── components/
│   ├── hooks/
│   ├── services/
│   └── store/
│
├── backend/
│   ├── src/
│   │   ├── auth/
│   │   ├── salons/
│   │   ├── practitioners/
│   │   ├── appointments/
│   │   ├── payments/
│   │   ├── waitlist/
│   │   ├── notifications/
│   │   └── analytics/
│   │
│   └── prisma/
│
├── jobs/
│   ├── reminders/
│   ├── waitlist/
│   ├── payments/
│   └── analytics/
│
├── docs/
│
└── docker/
```

---

## 📋 Core Modules

### Authentication

* JWT Authentication
* Refresh Tokens
* Role-Based Access Control

### Salon Management

* Salon Profiles
* Locations
* Ratings
* Reviews
* Photos

### Practitioner Management

* Skills
* Experience
* Availability
* Ratings

### Booking Engine

* Slot Generation
* Reservations
* Availability Validation
* Conflict Prevention

### Payments

* Deposits
* Full Payments
* Refunds
* No-show Fees

### Notifications

* SMS Alerts
* Email Notifications
* Booking Reminders

### Analytics

* Revenue Reports
* Peak Hour Analysis
* Stylist Performance
* Customer Retention

---

## 🔒 Handling Critical Edge Cases

### Concurrent Booking Protection

Prevents:

* Double bookings
* Race conditions
* Slot conflicts

Using:

* Database transactions
* Row-level locking
* Redis reservation locks

---

### Practitioner Sick Leave

Automatically:

* Blocks availability
* Cancels appointments
* Notifies customers
* Suggests alternative stylists

---

### Multi-Slot Services

Example:

60-minute haircut

Required slots:

```text
10:00 - 10:30
10:30 - 11:00
```

Adjacent slots are automatically reserved.

---

### Waitlist Handling

When cancellations occur:

1. Slot becomes available
2. Waitlist evaluated
3. Best customer selected
4. Notification sent instantly

---

## ⚡ Installation

### Clone Repository

```bash
git clone https://github.com/jyothsna2374/Salon-Scheduler-Development.git

cd Salon-Scheduler-Development
```

### Install Dependencies

```bash
npm install
```

### Environment Variables

Create:

```bash
.env
```

Example:

```env
DATABASE_URL=
REDIS_URL=

JWT_SECRET=

GOOGLE_MAPS_API_KEY=
GOOGLE_PLACES_API_KEY=

STRIPE_SECRET_KEY=

TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=

RESEND_API_KEY=
```

---

### Start Development

Frontend

```bash
npm run dev
```

Backend

```bash
npm run start:dev
```

---

## 🐳 Docker

Build containers:

```bash
docker-compose up --build
```

Run:

```bash
docker-compose up
```

Stop:

```bash
docker-compose down
```

---

## 🧪 Testing

Run unit tests:

```bash
npm run test
```

Run integration tests:

```bash
npm run test:e2e
```

Generate coverage:

```bash
npm run test:cov
```

---


## 👩‍💻 Author

### Jyothsna

Building intelligent scheduling systems powered by AI, automation, and scalable cloud architecture.
