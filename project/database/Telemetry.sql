CREATE TABLE "gym_capacity" (
  "id" serial PRIMARY KEY,
  "unit_id" integer,
  "location" varchar(255),
  "weather_id" int,
  "coordinate_id" int,
  "capacity" integer DEFAULT 0,
  "public_holiday" boolean DEFAULT false,
  "created_at" timestamp,
  "updated_at" timestamp
);

CREATE TABLE "weather" (
  "id" SERIAL PRIMARY KEY,
  "area" varchar(255),
  "deviceId" varchar(255),
  "rainfall" int,
  "forecast" varchar(255),
  "longitude" float,
  "latitude" float,
  "temperature" float,
  "time" timestamp
);

CREATE TABLE "coordinate" (
  "id" SERIAL PRIMARY KEY,
  "area" varchar(255) UNIQUE,
  "longitude" float,
  "latitude" float,
  "time" timestamp
);

CREATE TABLE "datacamp_courses" (
  "id" SERIAL PRIMARY KEY,
  "course_name" VARCHAR(50) UNIQUE NOT NULL,
  "course_instructor" VARCHAR(100) NOT NULL,
  "topic" VARCHAR(20) NOT NULL
);

COMMENT ON COLUMN "weather"."rainfall" IS 'TB1 Rainfall 5 Minute Total F in mm';

ALTER TABLE "gym_capacity" ADD FOREIGN KEY ("weather_id") REFERENCES "weather" ("id");

ALTER TABLE "gym_capacity" ADD FOREIGN KEY ("coordinate_id") REFERENCES "coordinate" ("id");
