-- CreateTable
CREATE TABLE "pokemon_diary" (
    "id" SERIAL NOT NULL,
    "user_id" INTEGER NOT NULL,
    "pokemon_name" TEXT NOT NULL,
    "notes" TEXT,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "pokemon_diary_pkey" PRIMARY KEY ("id")
);

-- AddForeignKey
ALTER TABLE "pokemon_diary" ADD CONSTRAINT "pokemon_diary_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "users"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
