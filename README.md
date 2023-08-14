# Wave

Caption and Translation API

### Build and Run the Docker Image Locally:

```$ docker compose -f local.yml build```

```$ docker compose -f local.yml up```

### Make local migrations:

```$ docker compose -f local.yml run --rm django python manage.py makemigrations```

```$ docker compose -f local.yml run --rm django python manage.py migrate```

### Docs:

```localhost:8000/api/v1/docs```

# Endpoints

## VideoViewSet: Taming Video Captioning With The Help of AI

Whether you're a frontend developer, backend wizard, or a unicorn enthusiast, welcome to the realm of video ednpoints! 🎥✨ Let's dive into the epic saga of handling videos in a way that even Gandalf would be proud of.

## Description

VideoViewSet is your trusty companion for managing videos like a pro. It's not just a view, it's a view with style and swagger, ready to slay dragons and transcribe videos. 🐉

### Methods

#### `create`

Use this mystical spell to create a new video with captions that even Shakespeare would envy.

- **HTTP Method:** POST
- **Path:** `/api/v1/videos/`

##### Wizard's Tip

Supply your media file and the type of task you want the video to perform. The sorcery behind the scenes will transcribe your video and craft you a magic response.

#### `partial_update`

Partial updates for when you need to give your video a makeover without breaking the spell.

- **HTTP Method:** PATCH
- **Path:** `/api/v1/videos/{id}/`

##### Wizard's Tip

Tweak the media path and captions of your video. Our wizards will ensure your updates are gracefully accepted or met with a `400 BAD REQUEST` spell.

#### `list`

Retrieve a list of your enchanted videos, safely guarded by your own user shield.

- **HTTP Method:** GET
- **Path:** `/api/v1/videos/`

##### Wizard's Tip

Paginate your way through your videos. Gather them in small, friendly clusters to avoid overwhelming even the bravest of browsers.

#### `retrieve`

Summon the details of a single video by invoking its unique identifier.

- **HTTP Method:** GET
- **Path:** `/api/v1/videos/{id}/`

##### Wizard's Tip

Retrieve the mystical knowledge of a specific video. The video's secrets shall be revealed in a splendid `200 OK` response.

## Sidekicks

Meet your trusty sidekicks, the powerful serializers, ready to translate your requests and responses between different dimensions.

- `VideoSerializer.Create`: Use this to channel your creativity when creating a video. Specify the task and language, and witness the magic unfold.
- `VideoSerializer.Get`: The master of ceremonies when revealing video secrets. This serializer unveils the beauty of a video.
- `VideoSerializer.List`: For those moments when you need to showcase your collection of videos. Tame the list with elegance.
- `VideoSerializer.Update`: When your video craves updates, this is your go-to spell. Adjust the media path and captions with grace.

Remember, brave developer, you are the commander of these views. May your APIs be as smooth as butter and your code as elegant as a dragon's dance. 🐲👩‍💻🚀



# PaymentViewSet: Level Up Your Video Quest with Payment Magic

Greetings, fellow adventurers of the WaveVerse! 🎮💰 Welcome to the realm of payments, where your heroic endeavors with videos are about to get a powerful upgrade. Gear up for an exhilarating journey as we blend the forces of videos and payments into one epic tale.

## The Chronicles Begin

Get ready to step into a world where videos meet payments in perfect harmony. payment emerges as your trusty guide, enhancing your WaveVerse experience like never before!

### Payment Sorcery

#### `create` - Enchanting Payments

Prepare to wield the ultimate spell to conjure payments that seamlessly integrate with your video conquests! ✨🧙‍♂️

- **Magic Scroll:** POST
- **Command:** `/api/v1/payments/`

##### Quest Tips

Channel your inner spellcaster to define the amount and payment plan. Our payment wizards will craft a seamless journey, complete with callbacks that align with your heroic quest.

#### `list` - Treasure Trove Unveiled

Embark on a treasure hunt that reveals the riches of your VideoVerse accomplishments, guarded by loyal pagination guardians! 🗺️📜

- **Explorer's Scroll:** GET
- **Command:** `/api/v1/payments/`

##### Quest Tips

Journey through the scrolls guided by our wise pagination guardians. Uncover your hard-earned treasures in bite-sized portions, making your exploration smooth and delightful.

#### `retrieve` - Unmask Payment Secrets

Venture deeper into the realm as you unveil the secrets behind individual payments, adding a layer of mystique to your adventure! 🔍🤐

- **Decoder Scroll:** GET
- **Command:** `/api/v1/payments/{id}`

##### Quest Tips

Empower yourself to unravel the essence of a single payment. The response shall reveal the secrets you seek, letting you savor the thrill of discovery.

### Guardians of Forbidden Paths

Beware, brave seeker! Some paths are forbidden, guarded by formidable sentinels.

- `update` and `partial_update`: These sacred records are untouchable, holding ancient power. Approach with respect. Forbidden: 403

- `destroy`: The fabric of the realm shudders at the thought of deletion. Honor the balance and tread carefully. Forbidden: 403

## Trusty Allies

Meet your allies, the valiant serializers, standing by to help you navigate this grand quest.

- `PaymentSerializers.Get`: Reveals the full scope of payment details.
- `PaymentSerializers.Fetch`: Fetches essential payment information, offering a taste of the adventure.

Fear not, brave developer! Your journey through the realms of videos and payments is about to reach new heights. May your callbacks resonate with victory and your code be as epic as the most legendary tales! 🌟🔮🚀
