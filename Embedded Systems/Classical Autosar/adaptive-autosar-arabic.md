# Adaptive AUTOSAR: من الصفر إلى الاحتراف

> الفكرة التي يقوم عليها هذا الدليل بسيطة:
> السيارة الحديثة لم تعد مجرد آلة ميكانيكية تتحكم فيها شرائح إلكترونية.
> أصبحت حاسوباً متحركاً يحتاج نظام تشغيل حقيقياً.
> سنبني هذا الفهم خطوة بخطوة.

---

## الجزء الأول: لماذا Adaptive AUTOSAR؟

### ابدأ بسؤال

تذكر آخر مرة استخدمت فيها تطبيق خرائط في سيارتك.

الخريطة تتحدث مع GPS.

تُدمج بيانات الكاميرات الأمامية.

تراقب الرادار لاكتشاف السيارات المجاورة.

تُحدَّث تلقائياً عبر الإنترنت.

وتعرض كل هذا على شاشة عالية الدقة.

```
هل يمكن لـ Classical AUTOSAR أن يفعل هذا؟

الجواب المختصر: لا.

Classical AUTOSAR صُمِّم لعالم مختلف:
← ECU المحرك ترسل 8 bytes كل 10ms على CAN
← Task يعمل كل 5ms بدقة مللي ثانية
← الكود ثابت ومعروف حجمه منذ يوم التصنيع
```

أما اليوم:

```
كاميرا واحدة فوق الزجاج الأمامي:
← تولّد ما بين 20 إلى 100+ ميجابايت من البيانات في كل ثانية
  (يعتمد على الدقة ومعدل الإطارات والضغط المستخدم)
← تحتاج معالجة بالذكاء الاصطناعي
← تتواصل مع السحابة
← تتلقى تحديثات بعد بيع السيارة

Classical AUTOSAR لم يصمَّم لهذا أصلاً.
```

هنا يأتي Adaptive AUTOSAR.

---

### ما الذي تغيّر في السيارات؟

بين عام 2005 وعام 2024، تغيّر شيء جوهري.

السيارة القديمة:

```
الوظيفة محددة من أول يوم
الكود لا يتغير بعد التصنيع
الاتصال بالعالم الخارجي: لا يوجد
السرعة المطلوبة: مللي ثانية
حجم البيانات: كيلوبايتات
```

السيارة الحديثة:

```
وظائف جديدة تُضاف بعد الشراء عبر OTA
الكود يتغير أسبوعياً (مثل هاتفك)
متصلة بالإنترنت دائماً
السرعة المطلوبة: معالجة الصورة في 50ms
حجم البيانات: جيجابايتات في الساعة
```

OTA = Over-The-Air Updates (التحديثات عبر الهواء).

هذا التحول هو سبب وجود Adaptive AUTOSAR.

---

### الفرق الجوهري بين Classical و Adaptive

قبل أن نمضي أكثر، هذه هي الصورة الكاملة:

```
┌────────────────────────────────────────────────────────────────┐
│              Classical AUTOSAR (CP)                            │
│                                                                │
│  يعمل على: Microcontroller (MCU) بسيط                        │
│  نظام التشغيل: OSEK-based OS (حتمي وبسيط)                   │
│  البرمجة: C فقط                                               │
│  الجدولة: ثابتة، تُحدَّد وقت التصميم                         │
│  التحديث: يحتاج فلاش كامل للـ ECU                            │
│  الذاكرة: كيلوبايتات إلى ميجابايتات                          │
│                                                                │
│  مناسب لـ: المحرك، الفرامل، ناقل الحركة                      │
└────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────┐
│              Adaptive AUTOSAR (AP)                             │
│                                                                │
│  يعمل على: Processor قوي (مثل ARM Cortex-A)                  │
│  نظام التشغيل: POSIX (مثل Linux أو QNX)                     │
│  البرمجة: C++14/17 بالأساس                                    │
│  الجدولة: ديناميكية، تتغير أثناء التشغيل                     │
│  التحديث: OTA بدون إيقاف كامل                                │
│  الذاكرة: جيجابايتات                                          │
│                                                                │
│  مناسب لـ: ADAS، الكاميرات، الرادار، الشاشات، السيارات       │
│            ذاتية القيادة                                       │
└────────────────────────────────────────────────────────────────┘
```

POSIX = Portable Operating System Interface (واجهة نظام التشغيل المحمولة).

ADAS = Advanced Driver Assistance Systems (أنظمة مساعدة السائق المتقدمة).

ملاحظة مهمة قبل أن نكمل:

```
Adaptive AUTOSAR لا يُلغي Classical AUTOSAR.

في السيارة الحديثة يعيشان معاً:

Classical ← يتحكم في المحرك والفرامل وكل ما يحتاج حتمية مضمونة
Adaptive  ← يشغّل الكاميرات والرادار وشاشة المعلومات والقيادة الذاتية
```

---

## الجزء الثاني: العتاد الذي يعمل عليه Adaptive

### ليس كل معالج يصلح

Classical AUTOSAR يعمل على Microcontroller بسيط:

```
Microcontroller (MCU) النموذجي:
← معالج بسيط (ARM Cortex-M4 مثلاً)
← ذاكرة Flash: 2 MB
← ذاكرة RAM: 256 KB
← لا يوجد نظام تشغيل معقد
← لا يوجد مُعالج رسوميات
← السعر: دولارات قليلة
```

Adaptive AUTOSAR يحتاج Processor مختلف تماماً:

```
High-Performance ECU (وحدة التحكم عالية الأداء):
← معالج قوي (مثل NVIDIA Orin, Qualcomm Snapdragon Ride)
← ذاكرة RAM: 8 GB إلى 64 GB
← تخزين: عشرات الجيجابايتات
← GPU للذكاء الاصطناعي
← شبكات اتصال سريعة (Automotive Ethernet 1Gbps/10Gbps)
← السعر: مئات الدولارات
```

GPU = Graphics Processing Unit (وحدة معالجة الرسوميات).

لكن لماذا GPU في سيارة؟

```
خوارزمية الكشف عن المشاة تحتاج:
← تحليل مليون بكسل في كل إطار
← 30 إطاراً في الثانية
← أي: 30 مليون عملية/ثانية على الأقل

CPU وحده: بطيء جداً لهذا
GPU: يعالج كل هذا بالتوازي في مللي ثانية
```

---

### SoC: دمج كل شيء في شريحة واحدة

SoC = System on Chip (نظام على شريحة).

تخيل أن لديك:

```
← CPU (قوي، متعدد الأنوية)
← GPU (للذكاء الاصطناعي)
← DSP (معالج إشارات رقمية)
← Memory Controller (للتحكم في الذاكرة)
← Network Interfaces (CAN, Ethernet, LIN)
← Security Module (وحدة الأمان)

كلها في شريحة واحدة.

هذا هو SoC.
```

أمثلة على SoCs المستخدمة في السيارات:

```
NVIDIA DRIVE Orin:
← 254 TOPS للذكاء الاصطناعي
← 12 أنوية ARM Cortex-A78AE
← GPU NVIDIA Ampere Architecture

Qualcomm Snapdragon Ride:
← مصمم خصيصاً للسيارات ذاتية القيادة
← يدعم AUTOSAR Adaptive مباشرة

Renesas R-Car H4:
← من أشهر SoCs في Automotive
← يدعم Functional Safety

Texas Instruments TDA4VM:
← للتطبيقات ADAS
← مزدوج: يحمل نظامي Classical و Adaptive معاً
```

TOPS = Tera Operations Per Second (تريليون عملية في الثانية).

---

### نظام التشغيل: POSIX

هذا الفرق الجوهري الأكبر بين Classical وAdaptive.

Classical يعمل فوق OSEK OS:

```
OSEK OS:
← أوامر قليلة جداً (Tasks, Alarms, Events)
← لا يوجد File System
← لا يوجد Network Stack
← لا يوجد Process Isolation
← الكل يتشارك نفس الذاكرة
← بسيط وحتمي ومضمون
```

Adaptive يعمل فوق POSIX OS:

```
POSIX OS (مثل Linux أو QNX أو Green Hills INTEGRITY):
← File System كامل
← Network Stack (TCP/IP)
← Processes منعزلة في الذاكرة
← Dynamic Linking (تحميل المكتبات أثناء التشغيل)
← Threads وScheduling متقدمة
← مألوف لأي مهندس برمجيات
```

QNX وLinux من أكثر أنظمة التشغيل استخداماً في Adaptive AUTOSAR اليوم.

QNX يتميز بطبيعته الحتمية وتاريخه الطويل في الأنظمة الحرجة، لذا تُفضّله كثير من شركات Tier-1 للأنظمة ذات المتطلبات الأمنية العالية.

Linux في المقابل بات منتشراً بشكل متزايد في منصات ADAS وHPDC، خاصة مع نمو نظم مثل NVIDIA DRIVE OS وAGL (Automotive Grade Linux).

الاختيار بين الاثنين يعتمد على الشركة، المنصة، ومتطلبات ASIL.

---

## الجزء الثالث: معمارية Adaptive AUTOSAR

### الصورة الكاملة أولاً

```
┌────────────────────────────────────────────────────────────────┐
│                    Adaptive Applications                       │
│                  (تطبيقات Adaptive AUTOSAR)                   │
│                                                                │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│   │  Application │  │  Application │  │  Application │       │
│   │    Process   │  │    Process   │  │    Process   │       │
│   │  (كاميرا)   │  │   (رادار)    │  │  (تخطيط مسار)│       │
│   └──────────────┘  └──────────────┘  └──────────────┘       │
├────────────────────────────────────────────────────────────────┤
│                 ARA (AUTOSAR Runtime for Adaptive)             │
│                   واجهة برمجة Adaptive                        │
│                                                                │
│  ┌─────────────┐  ┌────────────┐  ┌────────────┐              │
│  │ ara::com    │  │ ara::exec  │  │ ara::diag  │              │
│  │(اتصالات)   │  │(تنفيذ)     │  │(تشخيص)    │              │
│  └─────────────┘  └────────────┘  └────────────┘              │
│  ┌─────────────┐  ┌────────────┐  ┌────────────┐              │
│  │ ara::log    │  │ ara::crypto│  │ ara::per   │              │
│  │(تسجيل)     │  │(تشفير)     │  │(تخزين)    │              │
│  └─────────────┘  └────────────┘  └────────────┘              │
├────────────────────────────────────────────────────────────────┤
│                Adaptive Platform Foundation                    │
│                   (أساس المنصة Adaptive)                      │
│                                                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │ Execution    │  │ Communication│  │ State        │        │
│  │ Management  │  │ Management  │  │ Management  │        │
│  │ (مدير التنفيذ)│ │(مدير الاتصال)│  │(مدير الحالة) │        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
├────────────────────────────────────────────────────────────────┤
│               Operating System (POSIX / Linux / QNX)          │
│                     (نظام التشغيل)                            │
├────────────────────────────────────────────────────────────────┤
│                        Hardware                                │
│              (SoC / High-Performance ECU)                      │
└────────────────────────────────────────────────────────────────┘
```

المفهوم الجوهري:

```
في Classical:
البرنامج هو Task يعمل داخل OS

في Adaptive:
البرنامج هو Process مستقل (مثل برامج Linux)
لكل Process ذاكرته المعزولة
يتواصلون عبر ara::com
```

---

### الوحدة الأساسية: Adaptive Application

في Classical AUTOSAR الوحدة الأساسية هي SWC (Software Component).

في Adaptive AUTOSAR الوحدة الأساسية هي:

**Adaptive Application (التطبيق التكيّفي)**

وداخله:

**Service (الخدمة)**

```
Adaptive Application
└── يعمل كـ Process مستقل
    └── يُقدّم خدمة أو يستهلكها
        ├── Service Provider (مُقدّم الخدمة)
        │   مثل: خدمة بيانات الكاميرا الأمامية
        └── Service Consumer (مستهلك الخدمة)
            مثل: خدمة تخطيط المسار تستهلك بيانات الكاميرا
```

هذا النموذج اسمه: Service-Oriented Architecture (معمارية موجّهة بالخدمات).

SOA = Service-Oriented Architecture.

---

### SOA: بدلاً من الإشارات، نستخدم الخدمات

في Classical AUTOSAR:

```
SWC_Camera ──Signal (سرعة=3000)──► SWC_Display

Signal محدد من أول يوم التصميم
لا يمكن تغييره بدون إعادة تصميم كامل
```

في Adaptive AUTOSAR:

```
CameraService تُعلن:
"أنا أُقدّم خدمة اسمها CameraFeed"

DisplayService تبحث:
"هل هناك من يُقدّم CameraFeed؟"

الاتصال يحدث تلقائياً
بدون تحديد مسبق لمن يتحدث مع من
```

هذا يُمكّن شيئاً قوياً:

```
اليوم: Display يستهلك CameraFeed
بعد تحديث OTA: RecordingService يستهلك CameraFeed أيضاً

لا تغيير في كود CameraService على الإطلاق.
```

---

## الجزء الرابع: SOME/IP — لغة الاتصال

### ما قبل SOME/IP

في Classical AUTOSAR، اللغة الرئيسية هي CAN:

```
CAN:
← رسالة واحدة: 8 bytes كحد أقصى
← السرعة: حتى 1 Mbps
← البث لكل من على الشبكة
← مناسب: بيانات حساسات بسيطة
```

الآن تخيل نظام كاميرا:

```
كاميرا دقة 4K ترسل صورة:
← حجم الإطار: ~12 MB
← 30 إطاراً في الثانية
← إجمالي: 360 MB/s

CAN بـ 8 bytes لكل رسالة × 1 Mbps:
← يحتاج 45 مليون رسالة في الثانية
← مستحيل فيزيائياً
```

لذلك Adaptive AUTOSAR انتقل إلى Ethernet.

---

### SOME/IP (Scalable service-Oriented MiddlewarE over IP)

SOME/IP = البرمجيات الوسيطة القابلة للتوسع والموجّهة بالخدمات فوق IP.

هو البروتوكول الذي يجعل SOA تعمل في السيارة.

تخيّله كطبقة تُجيب على سؤال واحد:

```
"كيف يجد Service A الخدمة التي يحتاجها ويتحدث معها؟"
```

SOME/IP يحل هذا بثلاثة أجزاء:

---

#### الجزء الأول: Service Discovery (اكتشاف الخدمات)

تخيل سوقاً.

```
الباعة (Service Providers) يُعلنون:
"أبيع خضاراً" ، "أبيع ملابس" ، "أبيع إلكترونيات"

المشترون (Service Consumers) يبحثون:
"من يبيع خضاراً؟"

السوق يربطهم.
```

في SOME/IP:

```
CameraService تُرسل بث (Offer Service):
"أنا هنا، أُقدّم خدمة ID=0x0101"

DisplayService تبحث (Find Service):
"أبحث عن خدمة ID=0x0101"

SOME/IP SD يُعرّفهما ببعض
الاتصال يبدأ
```

SD = Service Discovery (اكتشاف الخدمات).

هذا يحدث تلقائياً دون أي إعداد مسبق يدوي.

---

#### الجزء الثاني: طرق الاتصال

SOME/IP يُقدّم ثلاث طرق للتواصل بين الخدمات:

**الأولى: Methods (الأساليب)**

مثل استدعاء دالة عن بُعد.

```
DisplayService تطلب من CameraService:
"أعطني الإطار الحالي"
    │
    ▼
CameraService ترد:
"هذا الإطار: [بيانات الصورة]"
```

في الكود:

```cpp
// العميل (Client Proxy)
auto result = cameraProxy.GetCurrentFrame().get();

// المزوّد (Skeleton)
Future<Frame> CameraService::GetCurrentFrame() {
    return MakeReadyFuture<Frame>(currentFrame_);
}
```

**الثانية: Events (الأحداث)**

بث مستمر بدون طلب.

```
CameraService ترسل كل 33ms تلقائياً:
"إطار جديد: [بيانات]"

كل من اشترك يستقبل
لا حاجة لطلب في كل مرة
```

هذا مثالي لبيانات الحساسات.

**الثالثة: Fields (الحقول)**

بيانات لها قيمة حالية يمكن قراءتها وتغييرها.

```
SpeedField في VehicleStatusService:
← يمكن قراءتها (Get)
← يمكن تغييرها (Set) — مع صلاحيات
← يُرسل إشعاراً عند التغيير (Notification)
```

---

#### الجزء الثالث: الشبكة — Automotive Ethernet

في Classical: CAN بسلكين.

في Adaptive: Automotive Ethernet.

```
100BASE-T1  ← 100 Mbps، سلكان مجدولان
1000BASE-T1 ← 1 Gbps، سلكان مجدولان
MultiGig    ← 2.5 / 5 / 10 Gbps

لماذا "سلكان مجدولان" مهمة في السيارة؟
← التجديل يُلغي التداخل الكهرومغناطيسي
← السيارة مليئة بمحركات ومولدات تُسبب ضجيجاً كهربائياً
```

---

### مقارنة CAN مع SOME/IP

```
┌──────────────────────────────────────────────────────────────┐
│                CAN (Classical)                               │
├───────────────┬──────────────────────────────────────────────┤
│ الحجم الأقصى │ 8 bytes (CAN) / 64 bytes (CAN-FD)           │
│ السرعة        │ 1 Mbps / 8 Mbps (CAN-FD)                    │
│ التوجيه       │ بث لكل من على الشبكة                        │
│ الاكتشاف      │ ثابت ومعروف مسبقاً                          │
│ الاستخدام     │ إشارات بسيطة (درجة حرارة، سرعة...)         │
└───────────────┴──────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│              SOME/IP (Adaptive)                              │
├───────────────┬──────────────────────────────────────────────┤
│ الحجم الأقصى │ عملياً غير محدود (TCP/UDP فوق Ethernet)     │
│ السرعة        │ 100 Mbps إلى 10 Gbps                        │
│ التوجيه       │ موجّه، من مزوّد لمشترك فقط                  │
│ الاكتشاف      │ ديناميكي وتلقائي                             │
│ الاستخدام     │ كاميرات، رادار، خدمات معقدة، OTA            │
└───────────────┴──────────────────────────────────────────────┘
```

---

## الجزء الخامس (أ): ara::core — الأساس الذي يُبنى عليه الكل

### لماذا ara::core تحديداً؟

كل كود Adaptive تكتبه يستخدم ara::core بشكل أو بآخر.

المشكلة أنها غير مرئية لأنها موجودة في كل مكان.

مثل الجاذبية — لا تلاحظها حتى تحاول تجاهلها.

---

### ara::core::Result — بديل الاستثناءات

في C++ العادي، الأخطاء تُعالَج بالاستثناءات:

```cpp
// C++ العادي
try {
    auto value = riskyOperation();
} catch (const std::exception& e) {
    handleError(e.what());
}
```

في Adaptive AUTOSAR، الاستثناءات ممنوعة في الكود الحرج.

لماذا؟

```
الاستثناءات تُسبّب:
← وقت تنفيذ غير متوقع (يكسر الحتمية)
← صعوبة في التحقق الرسمي لـ ASIL
← stack unwinding معقد وخطر

الحل: ara::core::Result
```

`Result<T, E>` هو حاوية تحمل إما:

```
نجاح (T): القيمة المطلوبة
فشل (E): رمز الخطأ

كأن الدالة تُرجع "الجواب أو سبب الفشل"
```

مثال عملي:

```cpp
#include "ara/core/result.h"
#include "ara/core/error_code.h"

// دالة تُرجع Result بدلاً من رمي استثناء
ara::core::Result<float> ReadTemperature(SensorId id) {
    if (!IsSensorAvailable(id)) {
        // فشل: أرجع كود الخطأ
        return ara::core::Result<float>::FromError(
            ara::core::ErrorCode{SensorErrors::kNotAvailable}
        );
    }
    
    float temp = ReadRawSensor(id);
    // نجاح: أرجع القيمة
    return ara::core::Result<float>{temp};
}

// كيف تستخدمها
void ProcessTemperature() {
    auto result = ReadTemperature(SensorId::CoolantTemp);
    
    if (result.HasValue()) {
        float temp = result.Value();
        // استخدم القيمة
    } else {
        auto error = result.Error();
        // تعامل مع الخطأ بدون استثناءات
        LogError(error.Message());
    }
    
    // أو بشكل أكثر إيجازاً:
    result.ValueOrThrow();        // يُرجع القيمة أو يرمي خطأ
    result.ValueOr(25.0f);        // يُرجع القيمة أو قيمة افتراضية
}
```

---

### ara::core::Future و Promise — الحساب اللامتزامن

هذا مفهوم مألوف من C++11، لكن له طعم مختلف في Adaptive.

تخيّل أنك طلبت طعاماً عبر تطبيق توصيل.

```
أنت (Consumer) تُرسل الطلب
لا تنتظر أمام الباب ساعتين
تُكمل يومك
عندما يصل الطعام: يُعلمك التطبيق
```

هذا هو المفهوم:

```cpp
// الطرف الأول: من يُنفّذ العملية (يُعطي Promise)
ara::core::Promise<RadarData> promise;
ara::core::Future<RadarData> future = promise.get_future();

// في Thread آخر أو Callback:
RadarData data = processRadar();
promise.set_value(data);  // "الطعام وصل"

// الطرف الثاني: من ينتظر النتيجة (يمسك Future)
future.then([](ara::core::Future<RadarData> f) {
    auto data = f.get();
    processFusionData(data);
});
// لا انتظار! البرنامج يُكمل عمله
```

**لماذا هذا مهم في الخدمات؟**

```
عندما يستدعي Proxy طريقة في Skeleton:
← الاستدعاء يعبر الشبكة (SOME/IP)
← قد يأخذ مللي ثانية أو أكثر

بدون Future: كل الـ Process تتجمد وتنتظر
مع Future: Process تُكمل عملها وترد عند وصول النتيجة
```

```cpp
// مثال كامل في ara::com
auto futureResult = radarProxy_->GetDetectedObjects();

// التطبيق يُكمل عمله بينما ينتظر الرد
doOtherWork();

// عندما نحتاج النتيجة فعلاً:
auto detection = futureResult.get();  // يتوقف هنا فقط لو لم تصل بعد
```

---

### ara::core::ErrorCode و ErrorDomain

كيف تُعرَّف الأخطاء في Adaptive؟

```
ErrorDomain = تصنيف الأخطاء (مثل namespace للأخطاء)
مثل: CoreErrorDomain, ComErrorDomain, PerErrorDomain

ErrorCode = رقم الخطأ + الـ Domain الذي ينتمي إليه
```

```cpp
// تعريف Domain خاص لخدمتك
enum class CameraErrors : ara::core::ErrorDomain::CodeType {
    kNotInitialized = 1,
    kFrameTimeout   = 2,
    kResolutionUnsupported = 3,
};

// استخدامه
ara::core::Result<Frame> CameraService::GetFrame() {
    if (!initialized_) {
        return ara::core::Result<Frame>::FromError(
            MakeErrorCode(CameraErrors::kNotInitialized)
        );
    }
    return Frame{currentFrame_};
}
```

---

### ara::core::InstanceSpecifier

هذا المفهوم يُربط كل شيء ببعض.

كيف يعرف التطبيق أنه يتحدث مع "الرادار الأمامي" وليس "الرادار الخلفي"؟

```cpp
// InstanceSpecifier يُعرَّف في Manifest ويُمرَّر للتطبيق
ara::core::InstanceSpecifier radarFrontSpecifier{
    "/vehicle/sensors/radar/front"
};

// الخدمة تُعلن عن نفسها بهذا المُعرِّف
radarService.OfferService(radarFrontSpecifier);

// المستهلك يبحث بنفس المُعرِّف
auto handles = RadarProxy::FindService(radarFrontSpecifier);
```

هذا يجعل النظام مرناً:

```
في Manifest ECU1: الرادار الأمامي في Instance "/vehicle/sensors/radar/front"
في Manifest ECU2: نفس الكود لكن Instance مختلف

نفس الكود يعمل في سيارات مختلفة بمجرد تغيير الـ Manifest
```

---



## الجزء الرابع (أ): Service Discovery بالتفصيل

### ما الذي يحدث فعلاً على الشبكة؟

SOME/IP-SD يعمل فوق UDP Multicast.

UDP = User Datagram Protocol (بروتوكول بيانات المستخدم).

Multicast = إرسال لمجموعة من المستقبلين دفعة واحدة.

تخيّل الأمر هكذا:

```
تدخل قاعة مليئة بالناس وتصرخ:
"هل يوجد أحد يُقدّم خدمة ترجمة؟"

من يُقدّمها يرد:
"أنا هنا، في الركن الأيمن، عنواني X"

الباقون يتجاهلون
```

SOME/IP-SD يفعل بالضبط نفس الشيء.

---

### دورة حياة الخدمة كاملة

**OfferService (الإعلان عن الخدمة):**

```
الـ Skeleton تستدعي OfferService()
    │
    ▼
SOME/IP-SD يُرسل Offer رسالة UDP Multicast:
{
  ServiceID: 0x0101,
  InstanceID: 0x0001,
  MajorVersion: 2,
  MinorVersion: 5,
  TTL: 3,          ← صلاحية الإعلان بالثانية
  IPv4Endpoint: "192.168.1.10:30490"
}
    │
    ▼
كل من على الشبكة يتلقى الرسالة
من يحتاجها يُسجّل العنوان
```

TTL = Time To Live (وقت الحياة) — الخدمة تُجدّد إعلانها قبل انتهاء الـ TTL.

**FindService (البحث عن الخدمة):**

```
المستهلك يريد خدمة Radar:

الحالة 1: الخدمة معلَنة بالفعل
← SOME/IP-SD يُرجع العنوان مباشرة من الـ cache

الحالة 2: الخدمة غير معلَنة بعد
← المستهلك يُرسل Find رسالة على الشبكة
← ينتظر Offer من أي مزوّد
← حين يصل Offer: يُنشئ الاتصال
```

**StopOfferService (إيقاف الخدمة):**

```
Skeleton تستدعي StopOfferService()
    │
    ▼
SOME/IP-SD يُرسل StopOffer رسالة:
{
  ServiceID: 0x0101,
  TTL: 0          ← TTL = 0 يعني: الخدمة لم تعد متاحة
}
    │
    ▼
كل المستهلكين يعلمون أن الخدمة توقفت
يحذفون الاتصال
```

---

### SubscribeEventgroup (الاشتراك في المجموعة)

Events في SOME/IP تُجمَّع في Eventgroups.

```
مثال: خدمة VehicleStatus تحتوي:

EventGroup 1: SensorData
├── SpeedEvent        ← كل 10ms
├── AccelerationEvent ← كل 20ms
└── SteeringEvent     ← عند التغيير

EventGroup 2: WarningAlerts
├── OverheatWarning
└── TirePressureWarning
```

المستهلك يشترك في Eventgroup كاملة:

```cpp
// Subscribe لـ EventGroup 1 فقط
proxy_->SensorDataEventGroup.Subscribe(
    ara::com::EventCacheUpdatePolicy::kLastN,
    10   // حجم الـ buffer
);

// الإشعار عند وصول بيانات جديدة
proxy_->SpeedEvent.SetReceiveHandler([this]() {
    auto samples = proxy_->SpeedEvent.GetNewSamples();
    // معالجة العينات
});
```

**Re-offer (تجديد الإعلان):**

```
المزوّد يُرسل Offer كل TTL/3 ثانية تقريباً:
← TTL = 3 ثانية → Offer كل ثانية

إذا لم يصل Offer في الوقت المحدد:
← المستهلك يعتبر الخدمة انتهت
← يبدأ البحث من جديد

هذا يكشف تعطّل الخدمة تلقائياً
```

---

### FindService Handle والاشتراك في التغييرات

```cpp
// البحث مرة واحدة
auto handles = RadarProxy::FindService(
    ara::core::InstanceSpecifier{"/sensors/radar/front"}
);

// أو: إشعار عند أي تغيير في توفر الخدمة
RadarProxy::StartFindService(
    [](ara::com::ServiceHandleContainer<RadarProxy::HandleType> handles,
       ara::com::FindServiceHandle findHandle) {
        
        if (!handles.empty()) {
            // الخدمة ظهرت
            auto proxy = std::make_shared<RadarProxy>(handles[0]);
        } else {
            // الخدمة اختفت
            proxy_.reset();
        }
    },
    ara::core::InstanceSpecifier{"/sensors/radar/front"}
);
```

هذا مهم في الأنظمة الحقيقية:

```
خدمة الرادار قد تتوقف وتُعاد فجأة:
← حزمة OTA جديدة
← إعادة تشغيل Process بعد خطأ

StartFindService يُعلمك تلقائياً
دون الحاجة لاستطلاع متكرر
```

---


---

## الجزء الرابع (ب): مكدس الاتصال الكامل

### الصورة التي تربط كل شيء ببعض

هذا هو السؤال الذي يسأله كل مهندس مبتدئ:

```
"بيانات الكاميرا تخرج من الـ Process وتدخل الشبكة.
ما الذي يحدث بينهما بالضبط؟"
```

الجواب:

```
┌────────────────────────────────────────────────────────────┐
│                     Application                            │
│         CameraService::SendFrame(frame)                    │
└──────────────────────────┬─────────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────────┐
│                    ara::com Layer                          │
│         يحزم البيانات في SOME/IP Message                  │
│         يُحدّد هل TCP أم UDP                              │
└──────────────────────────┬─────────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────────┐
│             Communication Management (CM)                  │
│         يُدير الاتصالات الفعلية                           │
│         يُطبّق SOME/IP Protocol                           │
│         يُضيف SOME/IP Header:                             │
│         [ServiceID][MethodID][Length][RequestID]          │
└──────────────────────────┬─────────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────────┐
│                    SOME/IP                                 │
│         بروتوكول التطبيق                                  │
│         يُعرّف شكل الرسالة                                │
└──────────────────────────┬─────────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────────┐
│                  TCP / UDP                                 │
│  Events صغيرة ← UDP (أسرع، بلا ضمان الوصول)             │
│  Methods حرجة ← TCP (مضمون الوصول، مع إعادة المحاولة)  │
└──────────────────────────┬─────────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────────┐
│                       IP                                  │
│         يُحدّد عنوان المصدر والوجهة (IPv4/IPv6)          │
└──────────────────────────┬─────────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────────┐
│               Ethernet Driver (MCAL في Adaptive)          │
│         يُحوّل الحزم لإشارات كهربائية                    │
└──────────────────────────┬─────────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────────┐
│                PHY (Physical Layer)                        │
│         الطبقة الفيزيائية الكهربائية                     │
│         100BASE-T1 أو 1000BASE-T1                        │
└──────────────────────────┬─────────────────────────────────┘
                           │
                      ═══════════
                       الكابل
                      ═══════════
```

---

### متى TCP ومتى UDP؟

هذا قرار مهم:

```
UDP ← بدون ضمان الوصول، لكن أسرع
يُستخدم مع:
← Events (بيانات دورية)
  "إطار الكاميرا كل 33ms"
  إذا فقدنا إطاراً واحداً لا مشكلة،
  الإطار التالي سيأتي خلال 33ms
← SOME/IP-SD (اكتشاف الخدمات)

TCP ← مضمون الوصول، مع ترتيب
يُستخدم مع:
← Methods (طلب/رد)
  "احسب لي المسار الأمثل"
  لا يُقبل أن تضيع
← Fields عند Set
  "غيّر سرعة المروحة إلى 80%"
  يجب أن تصل
```

---

### شكل SOME/IP Header

كل رسالة SOME/IP تبدأ بـ 16 byte من الـ header:

```
┌─────────────────────────────────────────────────────────┐
│  Byte 0-1:  Service ID       (معرّف الخدمة)            │
│  Byte 2-3:  Method/Event ID  (معرّف الأسلوب أو الحدث)  │
│  Byte 4-7:  Length           (طول البيانات التالية)     │
│  Byte 8-11: Request ID       (معرّف الطلب)             │
│  Byte 12:   Protocol Version (إصدار البروتوكول)        │
│  Byte 13:   Interface Version(إصدار الواجهة)           │
│  Byte 14:   Message Type     (نوع الرسالة)             │
│  Byte 15:   Return Code      (كود الرد)                │
└─────────────────────────────────────────────────────────┘
       ↓
   Payload (بيانات الرسالة المُتسلسَلة)
```

Message Types:

```
0x00 → REQUEST          (طلب يتوقع رداً)
0x01 → REQUEST_NO_RETURN(طلب لا يتوقع رداً)
0x02 → NOTIFICATION     (إشعار/Event)
0x80 → RESPONSE         (رد ناجح)
0x81 → ERROR            (رد بخطأ)
```

---


---

## الجزء الرابع (ج): DDS vs SOME/IP — المعركة الهادئة

### ما هو DDS؟

DDS = Data Distribution Service (خدمة توزيع البيانات).

هو معيار آخر لـ Middleware في الأنظمة الموزعة.

ليس وليداً من عالم السيارات — جاء من:

```
← الدفاع والجيش (أنظمة الرادار العسكرية)
← الفضاء (NASA يستخدمه)
← الروبوتيات (ROS 2 يعتمد عليه)
```

---

### مقارنة المفاهيم الأساسية

```
┌────────────────────────────────────────────────────────────────┐
│              SOME/IP                   DDS                     │
├─────────────────────────────────────────────────────────────────┤
│ نموذج الاتصال    │ Service-Oriented    │ Data-Centric          │
│ الاكتشاف         │ SOME/IP-SD          │ built-in (مدمج)       │
│ التسلسل          │ Custom Serialization│ CDR (CORBA Standard)  │
│ QoS              │ محدود               │ غني جداً (22+ Policy)│
│ المعيار          │ AUTOSAR             │ OMG Standard          │
│ الأداء (زمن وصول)│ جيد                 │ ممتاز                  │
│ Shared Memory    │ خارج المعيار        │ مدعوم مباشرة          │
│ انتشار في السيارات│ الأعلى (AUTOSAR)   │ متزايد                │
│ الأدوات          │ Vector, ETAS        │ RTI, Eclipse Cyclone  │
└────────────────────────────────────────────────────────────────┘
```

QoS = Quality of Service (جودة الخدمة).

CDR = Common Data Representation (تمثيل البيانات المشترك).

---

### ما الذي يجعل DDS مميزاً؟

**نظام QoS الغني:**

```
DDS يُتيح تحكماً دقيقاً مثل:

Reliability: ضمان وصول البيانات أم لا؟
Durability:  هل يُخزَّن آخر قيمة للمستهلكين الجدد؟
Deadline:    البيانات يجب أن تصل كل X ms أو خطأ
Liveliness:  كشف موت Publisher تلقائياً
History:     احتفظ بآخر N قيمة أو كل القيم
Ownership:   من يملك حق نشر هذه البيانات؟

كل هذا بسطر واحد في الكود
```

**لماذا هذا مهم في ADAS؟**

```
نظام Object Detection:
← ينشر مواقع الأجسام
← يجب وصول كل نشرة في < 50ms
← إذا تأخرت: هذا خطأ حرج (Deadline QoS)

نظام Lane Detection:
← ينشر خطوط الطريق
← متعدد Publishersvحسب الكاميرا
← من يملك نشر الخط المنتصف؟ (Ownership QoS)

DDS يحل هذا بشكل مدمج
SOME/IP يحتاج منطقاً إضافياً
```

---

### لماذا اختار AUTOSAR SOME/IP وليس DDS؟

السبب المنطقي: السياق التاريخي.

```
SOME/IP:
← طوّرته BMW وBosch للسيارات تحديداً (2011)
← متوافق مع بنية CAN الموجودة
← منتشر في الصناعة قبل Adaptive AUTOSAR
← الشركات لديها خبرة به بالفعل

DDS:
← جاء من خارج الصناعة
← يحتاج تعلماً جديداً
← أدواته أغلى وأقل توفراً
```

لكن المشهد يتطور:

```
AUTOSAR AP R20-11 وما بعده:
← أضافت دعماً رسمياً لـ DDS كـ binding بديل لـ ara::com
← يمكن بناء نظام Adaptive يعمل فوق DDS
← بدون تغيير كود التطبيق (فقط تبديل الـ binding)
```

---

### متى تختار أيهما؟

```
اختر SOME/IP إذا:
← تعمل في بيئة AUTOSAR AP خالصة
← الشبكة تحمل أجهزة بروتوكول CAN Gateway
← فريقك لديه خبرة AUTOSAR
← الأدوات المتاحة هي Vector أو ETAS

اختر DDS إذا:
← تتكامل مع نظام Robotics (مثل ROS 2)
← تحتاج QoS متقدماً جداً
← نظامك ينتشر خارج السيارة (V2X، Cloud)
← تستخدم Eclipse Cyclone DDS (مفتوح المصدر)

اختر الاثنين معاً إذا:
← سيارتك تتواصل مع بنية تحتية ذكية
← تحتاج Shared Memory داخل ECU (DDS)
  وشبكة خارجية بين ECUs (SOME/IP)
```

V2X = Vehicle to Everything (السيارة تتواصل مع كل شيء).

---


---

## الجزء الخامس: ARA — واجهة برمجة Adaptive AUTOSAR

### ما هو ARA؟

ARA = AUTOSAR Runtime for Adaptive.

هو مجموعة APIs يكتب عليها المهندس تطبيقه.

```
كما أن الـ RTE في Classical AUTOSAR هو الواجهة للـ SWC،
فإن ARA في Adaptive AUTOSAR هو الواجهة للـ Application.
```

الفرق:

```
Classical RTE:
← كود C بسيط
← مُولَّد تلقائياً
← Rte_Write / Rte_Read

Adaptive ARA:
← كود C++17
← مكتبات غنية بالـ namespace
← ara::com::proxy / ara::com::skeleton
```

---

### ara::com — طبقة الاتصال

هذه هي الطبقة التي يستخدمها المهندس للتواصل بين الخدمات.

تعمل بمفهومين:

**Proxy (الوكيل):**

```
ما يستخدمه مستهلك الخدمة (Consumer).

مثل: تطبيق يريد قراءة بيانات الرادار.
يستخدم RadarProxy للتحدث مع RadarService.

كأنه يتحدث مع الخدمة مباشرة
لكنه في الحقيقة يتحدث مع وكيل محلي
والوكيل يُوصّل عبر SOME/IP
```

**Skeleton (الهيكل):**

```
ما يستخدمه مُقدّم الخدمة (Provider).

مثل: خدمة الرادار نفسها.
تبني فوق RadarSkeleton لتُعلن عن نفسها وتردّ على الطلبات.
```

مثال عملي كامل:

```cpp
/* --- مُقدّم الخدمة (Provider / Skeleton) --- */

// ملف: radar_service.cpp
#include "ara/com/sample/radar_skeleton.h"

class RadarService : public ara::com::sample::RadarSkeleton {
public:
    RadarService(ara::com::InstanceIdentifier id)
        : RadarSkeleton(id) {}

    // ردّ على طلب GetDetectedObjects
    ara::core::Future<RadarDetection> GetDetectedObjects() override {
        RadarDetection detection;
        detection.numberOfObjects = currentDetections_.size();
        detection.objects = currentDetections_;
        return ara::core::MakeReadyFuture(detection);
    }

    // إرسال حدث دوري (Event)
    void SendUpdate(const RadarDetection& data) {
        DetectionEvent.Send(data);  // بث تلقائي لكل المشتركين
    }
};

int main() {
    RadarService service(ara::com::InstanceIdentifier{"Radar_Front"});
    service.OfferService();  // إعلان الخدمة على الشبكة
    
    while (running_) {
        RadarDetection data = processRadarSensor();
        service.SendUpdate(data);
        std::this_thread::sleep_for(std::chrono::milliseconds{50});
    }
    return 0;
}
```

```cpp
/* --- مستهلك الخدمة (Consumer / Proxy) --- */

// ملف: fusion_service.cpp
#include "ara/com/sample/radar_proxy.h"

class FusionService {
    std::shared_ptr<ara::com::sample::RadarProxy> radarProxy_;
    
public:
    void Initialize() {
        // البحث عن الخدمة
        auto handles = ara::com::sample::RadarProxy::FindService(
            ara::com::InstanceIdentifier{"Radar_Front"}
        );
        
        if (!handles.empty()) {
            radarProxy_ = std::make_shared<ara::com::sample::RadarProxy>(
                handles[0]
            );
            
            // الاشتراك في الحدث
            radarProxy_->DetectionEvent.Subscribe(10);  // buffer 10
            radarProxy_->DetectionEvent.SetReceiveHandler(
                [this]() { this->OnNewDetection(); }
            );
        }
    }
    
    void OnNewDetection() {
        auto samples = radarProxy_->DetectionEvent.GetNewSamples();
        for (auto& sample : samples) {
            processFusion(*sample);
        }
    }
};
```

---

### ara::exec — إدارة التنفيذ

Execution Management (إدارة التنفيذ) هي من أهم أجزاء Adaptive AUTOSAR.

في Classical AUTOSAR:

```
كل Tasks معروفة من وقت التصميم
تبدأ مع بداية الـ OS
لا تتغير أبداً
```

في Adaptive AUTOSAR:

```
التطبيقات تبدأ وتتوقف ديناميكياً
مثل processes في Linux

تريد تشغيل خدمة جديدة؟
← لا تحتاج إعادة تشغيل الـ ECU
← Execution Manager يُشغّلها
```

**Execution Manager (مدير التنفيذ):**

```
هو المسؤول عن:
← تشغيل الـ Adaptive Applications كـ Processes
← إيقافها بشكل آمن
← مراقبة حالتها
← استعادتها إذا تعطّلت
```

**Machine State (حالة الجهاز):**

Adaptive AUTOSAR يُعرّف حالات للجهاز (مثل حالات ECU في Classical):

```
Off      ← إيقاف تام
Startup  ← الإقلاع
Running  ← التشغيل الكامل
Shutdown ← الإغلاق الآمن
Update   ← تحديث OTA جارٍ
```

عند الانتقال بين الحالات:

```
Running → Update:
← Execution Manager يوقف التطبيقات غير الضرورية
← يبدأ تطبيق التحديث
← يُطبّق الحزمة الجديدة
← يُعيد التشغيل في Running
← كل هذا بدون إيقاف السيارة كاملاً
```


## الجزء الخامس (ب): دورة حياة التطبيق — من البداية للنهاية

### Execution Manager في العمق

سبق أن عرّفنا Execution Manager بشكل سريع.

الآن ندخل في التفاصيل التي تُسأل عنها في المقابلات.

---

### Process States (حالات العملية)

كل Adaptive Application تمر بحالات محددة:

```
                    ┌─────────────┐
                    │   Idle      │
                    │  (خامل)    │
                    └──────┬──────┘
                           │ Execution Manager يأمر بالتشغيل
                           ▼
                    ┌─────────────┐
                    │  Running    │
                    │  (يعمل)    │◄──────────────┐
                    └──────┬──────┘              │
                           │ طلب إيقاف          │ خطأ مؤقت
                           ▼                    │ أو إعادة تشغيل
                    ┌─────────────┐              │
                    │Terminating  │    ┌──────────┴───────┐
                    │(يتوقف...)  │    │   Error State    │
                    └──────┬──────┘    │    (خطأ)        │
                           │           └──────────────────┘
                           ▼
                    ┌─────────────┐
                    │ Terminated  │
                    │  (انتهى)   │
                    └─────────────┘
```

**الانتقالات:**

```
Idle → Running:
← Execution Manager يُطلق الـ Process
← يُمرّر له Instance Specifier من الـ Manifest
← التطبيق يُهيّئ نفسه ويُعلن عن خدماته

Running → Terminating:
← Execution Manager يُرسل إشارة إيقاف (SIGTERM في Linux)
← التطبيق يُغلق اتصالاته ويحفظ بياناته
← ينتهي في وقت محدد أو يُجبَر على الإنهاء

Running → Error:
← Process تعطّلت (Crash)
← PHM يُسجّل الخطأ
← يُقرر: إعادة تشغيل أم تصعيد الخطأ
```

---

### Function Groups — تشغيل انتقائي

هنا يكمن سحر Adaptive:

```
Function Group = مجموعة من Applications تعمل معاً في حالة معينة
```

مثال: سيارة تتنقل بين أوضاع مختلفة:

```
FunctionGroup: DrivingMode
├── State: Normal
│   └── Applications تعمل:
│       ← CameraService
│       ← RadarService
│       ← NavigationService
│
├── State: HighwayAutopilot
│   └── Applications تعمل:
│       ← CameraService
│       ← RadarService
│       ← NavigationService
│       ← LaneKeepingService   (جديد)
│       ← AdaptiveCruiseService (جديد)
│
└── State: ParkingMode
    └── Applications تعمل:
        ← UltrasonicService
        ← RearCameraService
        ← ParkingAssistService
        ← (الباقي موقوف توفيراً للطاقة)
```

**التحكم في Function Groups:**

```cpp
// طلب تغيير حالة Function Group
ara::exec::ExecutionClient executionClient;

// انتقل إلى وضع السريع
executionClient.RequestFunctionGroupState(
    ara::exec::FunctionGroup{"DrivingMode"},
    ara::exec::FunctionGroupState{"HighwayAutopilot"}
);

// Execution Manager يُشغّل ويوقف Applications حسب الحالة الجديدة
// دون تدخل من المهندس
```

---

### Startup Dependencies (تبعيات الإقلاع)

مشكلة واقعية:

```
FusionService تحتاج CameraService وRadarService قبل أن تبدأ.

كيف يضمن Execution Manager ترتيب الإقلاع؟
```

الجواب في Execution Manifest:

```json
{
  "applicationName": "FusionService",
  
  "startupDependencies": [
    {
      "functionGroup": "SensorDomain",
      "requiredState": "Running"
    }
  ]
}
```

```
Execution Manager يقرأ التبعيات:
    │
    ▼
يُشغّل CameraService وRadarService أولاً
    │
    ▼
ينتظر حتى يُعلنا جاهزيتهما (ReportExecutionState → kRunning)
    │
    ▼
يُشغّل FusionService
    │
    ▼
النظام جاهز
```

**كيف يُعلن التطبيق جاهزيته:**

```cpp
#include "ara/exec/execution_client.h"

int main() {
    // التهيئة
    auto camera = initializeCamera();
    auto comManager = initializeCom();
    
    // أعلن للـ Execution Manager أنك جاهز
    ara::exec::ExecutionClient execClient;
    execClient.ReportExecutionState(
        ara::exec::ExecutionState::kRunning
    );
    
    // الآن يمكن للخدمات التي تعتمد عليك أن تبدأ
    mainLoop();
    
    return 0;
}
```

---

### Machine Manifest — الإعداد الشامل للجهاز

سبق أن عرفنا Application Manifest.

Machine Manifest هو إعداد الجهاز كاملاً:

```
┌──────────────────────────────────────────────────────────────┐
│                   Manifest Files                             │
│                                                              │
│  Machine Manifest                                            │
│  ← إعدادات SoC كلها                                        │
│  ← الشبكات المتاحة (Ethernet, CAN...)                      │
│  ← Function Groups وحالاتها                                │
│  ← إعدادات الأمان والصلاحيات                               │
│                                                              │
│  Execution Manifest  (لكل Application)                      │
│  ← اسم التطبيق وإصداره                                     │
│  ← Process المطلوبة وخياراتها                              │
│  ← التبعيات والـ Function Group                            │
│  ← موارد CPU والذاكرة                                      │
│                                                              │
│  Service Instance Manifest (لكل خدمة)                      │
│  ← عناوين الشبكة                                            │
│  ← بروتوكول الاتصال (TCP/UDP)                              │
│  ← Instance ID المستخدم                                     │
│                                                              │
│  Service Interface Manifest (لكل واجهة)                    │
│  ← تعريف Methods, Events, Fields                           │
│  ← إصدار الواجهة                                            │
│  ← أنواع البيانات                                           │
└──────────────────────────────────────────────────────────────┘
```

مثال مبسّط لـ Execution Manifest:

```json
{
  "applicationName": "RadarService",
  "version": { "major": 2, "minor": 1, "patch": 0 },
  
  "process": {
    "executable": "/opt/radar/radar_service",
    "arguments": ["--config", "/etc/radar/radar.conf"],
    "schedulingPolicy": "SCHED_FIFO",
    "schedulingPriority": 80,
    
    "resourceGroups": [{
      "name": "RadarCPU",
      "cpuCores": [2, 3],
      "memoryLimit": "256MB"
    }]
  },
  
  "functionGroupState": {
    "functionGroup": "DrivingMode",
    "states": ["Normal", "HighwayAutopilot"]
  },
  
  "startupDependencies": [],
  
  "environmentalConditions": {
    "reportExecutionStateOnStartup": true
  }
}
```

---


---

### ara::diag — التشخيص في Adaptive

في Classical AUTOSAR، التشخيص يعمل عبر DCM وDEM.

في Adaptive AUTOSAR، الأساس نفسه (UDS لا يزال معياراً) لكن بمرونة أكبر:

```
ara::diag::DiagnosticService
← يستقبل طلبات UDS (الميكانيكي بأداة التشخيص)
← يرد بقيم الحساسات والأعطال

ara::diag::DiagnosticMonitor
← يُسجّل الأعطال (DTCs) مثل DEM في Classical
← لكن مع بيانات سياق أغنى بكثير

الفرق الأكبر:
في Classical: DEM بسيط ومحدود
في Adaptive: يمكن تسجيل مئات المتغيرات مع كل خطأ
مثل: الفيديو الذي كانت الكاميرا تلتقطه لحظة الحادث
```

---

### ara::per — التخزين الدائم

per = Persistency (الديمومة).

هو الطريقة التي يحفظ بها التطبيق بياناته بين تشغيلتين.

```
في Classical: NvM ← يحفظ في Flash أو EEPROM
في Adaptive: ara::per ← يحفظ في File System

مثال:
كاليبريشن نموذج الذكاء الاصطناعي للكاميرا
← تُحمَّل عند الإقلاع من ملف
← تُعدَّل مع الوقت
← تُحفَّظ عبر ara::per::WriteAccessor
```

---

### ara::log — التسجيل

في Classical: DET (Development Error Tracer) بسيط جداً.

في Adaptive: ara::log مع إمكانيات كاملة:

```cpp
#include "ara/log/logger.h"

auto logger = ara::log::CreateLogger("CAM", "Camera Service");

// مستويات التسجيل
logger.LogDebug() << "بدأ تهيئة الكاميرا";
logger.LogInfo()  << "الكاميرا تعمل بدقة " << resolution_;
logger.LogWarn()  << "جودة الصورة منخفضة بسبب الإضاءة";
logger.LogError() << "فشل الاتصال بالكاميرا: " << errorCode;
logger.LogFatal() << "خطأ حرج — إيقاف الخدمة";
```

البيانات يمكن إرسالها للسحابة لتحليلها لاحقاً.

---

### ara::crypto — الأمان والتشفير

السيارة المتصلة بالإنترنت = هدف للقراصنة.

ara::crypto يُوفّر:

```
← تشفير وفكّ تشفير البيانات (AES, RSA)
← التوقيع الرقمي (ECDSA)
← التحقق من صحة حزم OTA
← إدارة المفاتيح
← Secure Boot (الإقلاع الآمن)
```

مثال عملي: كيف يتحقق Adaptive من حزمة OTA:

```
خادم الشركة يُرسل حزمة تحديث:
    │
    ▼
الحزمة مُوقَّعة بمفتاح خاص (Private Key) عند الشركة
    │
    ▼
ara::crypto تتحقق بالمفتاح العام (Public Key) المُخزَّن في السيارة
    │
    ▼
إذا التوقيع صحيح: تُنصَّب الحزمة
إذا التوقيع خاطئ: ترفض وتُسجّل محاولة اختراق
```

---

## الجزء السادس: القيادة الذاتية وADAS

### لماذا القيادة الذاتية تحتاج Adaptive؟

هذه هي الحجة الأقوى لوجود Adaptive AUTOSAR.

تخيّل ما يحتاجه نظام القيادة الذاتية:

```
الإدراك (Perception):
← كاميرات متعددة → معالجة صورة بالذكاء الاصطناعي
← Lidar → معالجة سحابة النقاط ثلاثية الأبعاد
← Radar → كشف الجسيمات وقياس سرعتها
← مجسات الموجات فوق الصوتية → للمناطق القريبة

إجمالي البيانات: عشرات الجيجابايتات في الساعة
```

```
الفهم (Understanding):
← أين نحن بالضبط؟ (Localization)
← ما هي الأشياء حولنا؟ (Object Detection)
← ماذا ستفعل السيارات الأخرى؟ (Behavior Prediction)

يحتاج: GPU وShared Memory بين Processes
```

```
التخطيط (Planning):
← ما المسار الأمثل؟
← متى نتجاوز؟ متى نتوقف؟
← كيف نتعامل مع الحالات الطارئة؟

يحتاج: حسابات معقدة في مللي ثانية
```

```
التحكم (Control):
← ترجمة القرارات إلى أوامر للمحرك والفرامل والتوجيه

هنا يتدخل Classical AUTOSAR مجدداً.
```

---

### مستويات القيادة الذاتية

SAE = Society of Automotive Engineers (جمعية مهندسي السيارات).

```
Level 0 — لا أتمتة:
السائق يتحكم في كل شيء
المساعد الوحيد: تحذيرات صوتية

Level 1 — مساعدة واحدة:
إما التوجيه أو السرعة، ليس الاثنين
مثال: Cruise Control (تثبيت السرعة)

Level 2 — أتمتة جزئية:
التوجيه والسرعة معاً في بعض الأحيان
السائق يجب أن يراقب دائماً
مثال: Tesla Autopilot، Mercedes Drive Pilot

Level 3 — أتمتة مشروطة:
السيارة تقود في ظروف محددة
السائق لا يحتاج المراقبة لكن يجب الاستجابة عند الطلب
نادر في السوق حالياً

Level 4 — أتمتة عالية:
لا يحتاج سائقاً في ظروف محددة (مدينة معينة، طريق سريع)
Waymo Robotaxi هو المثال الأبرز

Level 5 — أتمتة كاملة:
في كل الظروف، في كل مكان
لم يصل إليه أحد بعد
```

Adaptive AUTOSAR هو العمود الفقري لـ Level 2 وما فوق.

---

### بنية نظام ADAS

```
┌────────────────────────────────────────────────────────────────┐
│                    Sensor Layer                                │
│                  (طبقة الحساسات)                              │
│                                                                │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐         │
│  │ Camera   │ │  Lidar   │ │  Radar   │ │   USS    │         │
│  │ Service  │ │ Service  │ │ Service  │ │ Service  │         │
│  └─────┬────┘ └─────┬────┘ └─────┬────┘ └─────┬────┘         │
│        │            │            │            │               │
│  ══════╪════════════╪════════════╪════════════╪══════         │
│                    SOME/IP over Ethernet                       │
│  ══════╪════════════╪════════════╪════════════╪══════         │
│        │            │            │            │               │
├────────┴────────────┴────────────┴────────────┴───────────────┤
│                    Fusion Layer                                │
│                  (طبقة الدمج)                                 │
│                                                                │
│         ┌────────────────────────────────┐                    │
│         │    Sensor Fusion Service       │                    │
│         │   (دمج بيانات كل الحساسات)    │                    │
│         └────────────────────────────────┘                    │
│                          │                                     │
├──────────────────────────┼────────────────────────────────────┤
│                    Perception Layer                            │
│                  (طبقة الإدراك)                               │
│                                                                │
│   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐   │
│   │  Object      │    │  Lane        │    │  Traffic     │   │
│   │  Detection   │    │  Detection   │    │  Sign Recog  │   │
│   │  Service     │    │  Service     │    │  Service     │   │
│   └──────────────┘    └──────────────┘    └──────────────┘   │
├────────────────────────────────────────────────────────────────┤
│                    Planning Layer                              │
│                  (طبقة التخطيط)                               │
│                                                                │
│           ┌────────────────────────────────┐                  │
│           │    Path Planning Service       │                  │
│           │   (تخطيط المسار)              │                  │
│           └────────────────────────────────┘                  │
├────────────────────────────────────────────────────────────────┤
│                    Control Layer                               │
│                  (طبقة التحكم)                                │
│                          │                                     │
│              ┌───────────┴───────────┐                        │
│         Classical AUTOSAR        Classical AUTOSAR             │
│         Engine/Brake ECU         Steering ECU                  │
└────────────────────────────────────────────────────────────────┘
```

USS = Ultrasonic Sensors (حساسات موجات فوق صوتية).

---

## الجزء السابع: OTA — تحديثات ما بعد البيع

### هذا ما يُغيّر كل شيء

قبل Adaptive AUTOSAR، كيف كنت تُحدّث سيارة؟

```
← تذهب للوكيل
← الميكانيكي يوصل كابل خاص
← يُنزّل ملف التحديث
← العملية تأخذ ساعة أو أكثر
← أحياناً لا تُحدَّث السيارة أبداً
```

مع Adaptive AUTOSAR:

```
السيارة متصلة بشبكة الجوال (4G/5G)
    │
    ▼
خوادم الشركة تُرسل حزمة تحديث
    │
    ▼
ara::ucm تستقبلها (UCM = Update and Configuration Management)
    │
    ▼
التحقق من التوقيع الرقمي (ara::crypto)
    │
    ▼
التنزيل في الخلفية (السيارة تعمل بشكل طبيعي)
    │
    ▼
بعد إيقاف السيارة: تُطبَّق التحديثات
    │
    ▼
في الصباح: وظائف جديدة
```

مثال توضيحي (التفاصيل الدقيقة تختلف من إصدار لآخر):

```
تحديثات OTA في السيارات الحديثة (Tesla, BMW, Mercedes...):
← إضافة ميزات قيادة مساعِدة جديدة
← تحسين كفاءة البطارية
← تعديل سلوك نظام الصوت والشاشات
← إصلاح ثغرات أمنية برمجياً

كل هذا بدون زيارة الوكيل.
```

---

### كيف يعمل UCM

UCM = Update and Configuration Management.

```
المراحل:
1. TransferStart: بدء نقل الحزمة
2. TransferData: نقل البيانات
3. TransferExit: انتهاء النقل
4. ProcessSwPackage: معالجة وتثبيت الحزمة
5. Activate: تفعيل التحديث (عند الإقلاع التالي)
6. Rollback: العودة للإصدار السابق إذا فشل شيء
```

Rollback (التراجع) مهم جداً:

```
التحديث يُطبَّق
    │
    ▼
ECU يُقلع بالإصدار الجديد
    │
    ▼
نظام يتحقق: هل كل شيء يعمل؟
    │
    ├── نعم ← يُثبَّت التحديث نهائياً
    │
    └── لا (خطأ أو عطل) ← Rollback تلقائي للإصدار القديم
        السيارة تعود تعمل بالإصدار القديم الموثوق
```

هذا يضمن أن السيارة لن "تتعطل" بسبب تحديث فاشل.

---

## الجزء الثامن: الأمان الوظيفي في Adaptive

### ISO 26262 لا يختفي

ذكرنا في Classical AUTOSAR أن ISO 26262 هو معيار الأمان.

في Adaptive AUTOSAR هو لا يزال مطلوباً، لكن هناك تحدٍ:

```
Classical:
← كود محدود وثابت
← يمكن إثبات سلامته رياضياً
← ASIL D ممكن

Adaptive:
← نظام تشغيل ديناميكي
← عمليات تبدأ وتنتهي
← OTA يُغيّر السلوك
← ASIL D الكامل أصعب بكثير
```

لذلك الحل العملي في الصناعة:

```
السيارة الحديثة تُقسَّم:

Zone A (ASIL D): Classical AUTOSAR
← الفرامل، التوجيه، المحرك
← لا OTA، لا ديناميكية
← إثبات السلامة أبسط وأكثر نضجاً

Zone B (ASIL B/C/D جزئي): Adaptive AUTOSAR — الحرجة
← يمكن تحقيق ASIL مع جهد إضافي في التحقق والتحقق الرسمي
← نظام المساعدة في المسار (Lane Assist)
← التحكم في السرعة التكيفي (ACC)
← يتطلب: Freedom from Interference + تقسيم صارم للذاكرة

Zone C (QM): Adaptive AUTOSAR — غير الحرجة
← الشاشة والترفيه
← خدمات الإنترنت والخرائط
← يمكن أن يتعطل بدون خطر على الحياة
```

ACC = Adaptive Cruise Control (تثبيت السرعة التكيّفي).

---

### Platform Health Management (PHM) — قسم مستقل

PHM = Platform Health Management (إدارة صحة المنصة).

هو الـ WdgM في عالم Adaptive — لكن أكثر تطوراً وأعمق مسؤولية.

---

**لماذا يوجد PHM أصلاً؟**

في Classical AUTOSAR:

```
النظام بسيط:
← Tasks معروفة من أول يوم
← إذا تجمّدت Task: Watchdog يُعيد تشغيل ECU
← كل شيء في process واحدة
```

في Adaptive AUTOSAR:

```
النظام أكثر تعقيداً:
← عشرات الـ Processes المستقلة
← كل Process قد تتعطل بشكل مختلف
← بعض العطل حرجة تستوجب إيقاف السيارة
← بعضها عارضة تحلّها إعادة تشغيل Process واحدة

إعادة تشغيل الـ SoC كله لكل خطأ = غير مقبول.
```

PHM يحل هذا بذكاء.

---

**المكوّنات الأساسية لـ PHM:**

```
┌─────────────────────────────────────────────────────────────────┐
│                    Platform Health Management                   │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Health Channel (قناة الصحة)                             │   │
│  │  ← يستقبل تقارير الصحة من كل Application              │   │
│  │  ← يُحدّد: هل هذه التقارير ضمن الحد الزمني؟           │   │
│  └──────────────────────┬───────────────────────────────────┘   │
│                         │                                       │
│  ┌──────────────────────▼───────────────────────────────────┐   │
│  │  Supervision (الإشراف)                                   │   │
│  │  ← يُقيّم حالة كل Supervised Entity                    │   │
│  │  ← ثلاثة أنواع من الإشراف:                            │   │
│  │    1. Alive Supervision    (هل لا يزال حياً؟)          │   │
│  │    2. Deadline Supervision (هل أنجز في الوقت؟)         │   │
│  │    3. Logical Supervision  (هل التسلسل صحيح؟)          │   │
│  └──────────────────────┬───────────────────────────────────┘   │
│                         │                                       │
│  ┌──────────────────────▼───────────────────────────────────┐   │
│  │  Recovery Action (إجراء الاسترداد)                       │   │
│  │  ← يُقرر ماذا يفعل بناءً على نوع وخطورة الخطأ         │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

**الأنواع الثلاثة للإشراف:**

**1. Alive Supervision (إشراف الحياة):**

```
المبدأ: نفس Watchdog الكلاسيكي لكن على مستوى Process

التطبيق يُرسل "أنا حي" بشكل دوري:
    │
    ▼
PHM يتحقق: هل وصلت ضمن الإطار الزمني؟
    │
    ├── وصلت → Process بصحة جيدة
    └── لم تصل → Process ربما تجمّدت → تصعيد الخطأ
```

كيف يُرسل التطبيق إشارة الحياة:

```cpp
#include "ara/phm/supervised_entity.h"

// في منطقة الكود التي يجب أن تُنفَّذ بشكل دوري
ara::phm::SupervisedEntity supervisedEntity{
    ara::core::InstanceSpecifier{"/radar/main_loop"}
};

void MainLoop() {
    while (running_) {
        processRadarData();

        // أرسل لـ PHM: "أنا هنا وأعمل بشكل طبيعي"
        supervisedEntity.ReportCheckpoint(
            ara::phm::CheckpointId{1}
        );

        std::this_thread::sleep_for(std::chrono::milliseconds{50});
    }
}
```

**2. Deadline Supervision (إشراف الميعاد):**

```
المبدأ: ليس فقط "هل وصلت؟" بل "هل وصلت في الوقت الصحيح؟"

يُحدَّد: Checkpoint A يجب أن يأتي بعد Checkpoint B بين 10ms و 50ms

إذا جاء أبكر من 10ms → خطأ (النظام يعمل بشكل أسرع من المتوقع)
إذا جاء بعد 50ms → خطأ (النظام يعمل أبطأ من المتوقع)
```

```cpp
// Checkpoint عند بداية العملية
supervisedEntity.ReportCheckpoint(ara::phm::CheckpointId{1}); // Start

performHeavyComputation();

// Checkpoint عند الانتهاء
supervisedEntity.ReportCheckpoint(ara::phm::CheckpointId{2}); // End
// PHM يحسب الوقت بين 1 و 2 ويتحقق أنه ضمن النطاق المسموح
```

**3. Logical Supervision (الإشراف المنطقي):**

```
المبدأ: التحقق من أن تسلسل Checkpoints منطقي وصحيح

مثال: خوارزمية لها خطوات محددة
A → B → C → D

إذا جاء تسلسل A → C مباشرة: خطأ منطقي
إذا جاء D قبل A: خطأ منطقي

يكشف: الحلقات اللانهائية، التخطي غير المقصود للخطوات الحرجة
```

---

**Recovery Actions — ماذا يفعل PHM عند الخطأ؟**

هذا هو قلب PHM.

ليس كل خطأ يستوجب نفس الاستجابة:

```
┌─────────────────────────────────────────────────────────────────┐
│              مستويات خطورة الخطأ وإجراءات الاسترداد            │
│                                                                 │
│  الخطأ بسيط وعابر                                              │
│  ← PHM ينتظر دورة أخرى                                        │
│  ← إذا تكرر: ينتقل للمستوى التالي                             │
│                          │                                      │
│                          ▼                                      │
│  الخطأ متكرر في Process واحدة                                  │
│  ← Execution Manager يُعيد تشغيل هذه الـ Process فقط          │
│  ← باقي الـ Processes تستمر                                   │
│  ← يُسجّل في ara::log وara::diag                              │
│                          │                                      │
│                          ▼                                      │
│  Process لا تستجيب حتى بعد إعادة التشغيل                      │
│  ← PHM يُغيّر حالة Function Group                             │
│  ← يُوقف مجموعة الـ Applications المتعلقة                     │
│  ← يُبلّغ State Management                                    │
│                          │                                      │
│                          ▼                                      │
│  خطأ حرج يهدد السلامة                                          │
│  ← إيقاف الـ SoC بالكامل                                      │
│  ← Classical AUTOSAR يُفعَّل                                   │
│  ← (الفرامل والتوجيه تظل تعمل بشكل مستقل)                   │
└─────────────────────────────────────────────────────────────────┘
```

---

**PHM وFreedom from Interference:**

هذا مفهوم ISO 26262 مهم جداً في Adaptive:

```
Freedom from Interference (الحرية من التداخل):
← Process ASIL B لا يجب أن تؤثر على Process ASIL D
← حتى لو تعطّلت Process QM، الـ Process الحرجة تظل تعمل

PHM يُحقق هذا بـ:
← Process Isolation (الـ OS يعزل الذاكرة)
← CPU Partitioning (نوى CPU مخصصة لـ ASIL العالي)
← Memory Partitioning (مناطق ذاكرة منفصلة)
← Time Partitioning (وقت CPU مضمون للـ ASIL العالي)

المصطلح الجامع: Mixed-Criticality System
```

---

**PHM مقارنةً بـ WdgM في Classical:**

```
┌──────────────────────────────────────────────────────────────┐
│           Classical WdgM          │         Adaptive PHM     │
├──────────────────────────────────┼──────────────────────────┤
│ يراقب Runnables                   │ يراقب Processes          │
│ إشارة حياة بسيطة                  │ ثلاثة أنواع إشراف       │
│ إعادة تشغيل ECU كله              │ استجابة متدرجة ذكية      │
│ يعمل في Process واحدة             │ يُدير عشرات الـ Processes│
│ لا يعرف شيئاً عن الـ Logic       │ يفهم تسلسل الـ Checkpoints│
│ بسيط ومضمون                       │ مرن وأكثر تعبيراً       │
└──────────────────────────────────┴──────────────────────────┘
```

---



---

### AUTOSAR Adaptive وAUTOSAR Classic يتعاونان: E2E

E2E Protection (الحماية من النهاية إلى النهاية) موجودة في الاثنين.

```
في Classic على CAN:
← CRC + Counter على كل Signal حرج
← يحمي من التشويه الكهرومغناطيسي

في Adaptive على SOME/IP:
← نفس المفهوم لكن فوق UDP
← SOME/IP-E2E يُضيف Header خاص للتحقق
← يحمي من أخطاء الشبكة وهجمات التلاعب
```


## الجزء التاسع (أ): إدارة الذاكرة — Zero-Copy وShared Memory

### المشكلة التي لا يذكرها أحد

تخيّل إطار كاميرا 4K (مثال توضيحي — الأرقام الحقيقية تتفاوت حسب الضغط والتشفير):

```
4K Frame بدون ضغط:
← 3840 × 2160 بكسل
← 3 قنوات لون (RGB)
← 8 bits لكل قناة
← الحجم التقريبي: ~25 MB لكل إطار

بـ 30 إطاراً في الثانية: ~750 MB/s كحد أقصى نظري
(مع الضغط مثل H.265: ينخفض كثيراً — لكن معالجة الضغط نفسها تكلفة)
```

الآن تخيّل أن FusionService تريد هذا الإطار:

**الطريقة التقليدية (Copy):**

```
CameraService           FusionService
     │                      │
     │  1. بيانات في ذاكرة Camera Process
     │                      │
     │  2. نسخ إلى SOME/IP buffer
     │                      │
     │  3. إرسال عبر TCP/UDP (كود النواة يتدخل)
     │         Network       │
     │  4. استقبال في FusionService
     │                      │
     │  5. نسخ إلى ذاكرة Fusion Process
     │                      │
```

هذا يعني نسخ ~25 MB ثلاث مرات في كل إطار.

```
ثلاث نسخ × 30 إطار × ~25 MB ≈ أكثر من 2 GB/s من نسخ الذاكرة فقط!
(في أحسن الأحوال بدون ضغط — لكن المبدأ يبقى صحيحاً حتى مع الضغط)
```

وحدها تستهلك موارد ضخمة وتُضيف تأخيراً.

---

### Shared Memory — الحل الأنيق

بدلاً من النسخ، نُشارك نفس المنطقة في الذاكرة:

```
CameraService           FusionService
     │                      │
     │    ┌─────────────────────────┐
     │    │     Shared Memory       │
     │    │      (منطقة مشتركة)    │
     │    │                         │
     │    │  [Frame Buffer 1] ◄─────┼─── يقرأ
     │    │  [Frame Buffer 2]       │
     │    │  [Frame Buffer 3]       │
     │    └─────────────────────────┘
     │         ↑
     │    يكتب هنا مباشرة
```

**نتيجة:**

```
بدون نسخ.
CameraService يكتب مرة.
FusionService يقرأ من نفس الموقع.
التأخير: مللي ثانية أو أقل.
استهلاك الذاكرة: مرة واحدة فقط.
```

---

### Zero-Copy في ara::com

AUTOSAR Adaptive يدعم Zero-Copy بآلية خاصة:

**Loaned Samples (العينات المُعارة):**

```cpp
// في مُقدّم الخدمة (Skeleton)
// بدلاً من إنشاء نسخة جديدة من البيانات:

// الطريقة العادية (مع نسخ):
Frame myFrame = buildFrame();
DetectionEvent.Send(myFrame);   // ينسخ myFrame

// الطريقة Zero-Copy:
auto loanedSample = DetectionEvent.Allocate();  // احجز مساحة في Shared Memory
auto& frame = loanedSample.Value();
fillFrame(frame);  // اكتب مباشرة في Shared Memory
DetectionEvent.Send(std::move(loanedSample));  // لا نسخ!
```

```cpp
// في مستهلك الخدمة (Proxy)
proxy_->DetectionEvent.SetReceiveHandler([&]() {
    auto samples = proxy_->DetectionEvent.GetNewSamples(
        [](auto& sample) {
            // sample يُشير مباشرة إلى Shared Memory
            // لا نسخ حتى هنا!
            processFrame(*sample);
        },
        10  // حد أقصى 10 عينات
    );
});
```

---

### متى تستخدم Shared Memory ومتى لا؟

```
استخدم Shared Memory / Zero-Copy مع:
← البيانات الكبيرة (> 1 KB)
← الإطارات من الكاميرات والـ Lidar
← بيانات التدفق المستمر
← الـ Processes على نفس الـ SoC

لا تستخدمه مع:
← البيانات الصغيرة (أصغر من الـ overhead)
← الـ Processes على ECUs مختلفة (مستحيل)
← الاتصالات الخارجية عبر الشبكة
← الحالات التي تحتاج ASIL عالي (يُعقّد التحقق)
```

---

### Huge Buffers وتجنّب TLB Misses

في الأنظمة الحقيقية لمعالجة الصور، تُستخدم Huge Pages:

```
الذاكرة العادية: تُقسَّم إلى صفحات 4 KB
مشكلة: كل وصول لصفحة جديدة يحتاج TLB lookup
مع 24 MB frame: آلاف التحويلات في كل إطار = بطء

الحل: Huge Pages (2 MB أو 1 GB للصفحة)
← أقل TLB misses
← معالجة أسرع للإطارات الكبيرة
← يُعدَّل في Machine Manifest أو OS config
```

TLB = Translation Lookaside Buffer (مخزن ترجمة العناوين).

---


---

## الجزء التاسع (ب): رحلة التطبيق من الكود إلى السيارة

### الصورة الكاملة لدورة التطوير والنشر

هذه رحلة كل Application Adaptive من أول سطر كود حتى تشتغل في السيارة:

```
┌────────────────────────────────────────────────────────────────┐
│  1. Development (التطوير)                                      │
│                                                                │
│  المهندس يكتب:                                                 │
│  ← تصميم الخدمة في .arxml                                     │
│  ← كود C++ فوق Skeleton / Proxy المُولَّد                     │
│  ← يكتب الـ Manifest files                                    │
│                                                                │
│  الأدوات: CLion / VS Code + CMake + AUTOSAR SDK              │
└──────────────────────────────┬─────────────────────────────────┘
                               │
                               ▼
┌────────────────────────────────────────────────────────────────┐
│  2. Build (البناء)                                             │
│                                                                │
│  CMake يبني:                                                   │
│  ← تحويل .arxml إلى Skeleton/Proxy (Code Generator)          │
│  ← ترجمة C++ لـ target architecture (ARM cross-compile)      │
│  ← ربط المكتبات (ara:: libraries)                            │
│                                                                │
│  الناتج: ملف قابل للتنفيذ (ELF binary) + Manifests          │
└──────────────────────────────┬─────────────────────────────────┘
                               │
                               ▼
┌────────────────────────────────────────────────────────────────┐
│  3. Packaging (التغليف)                                        │
│                                                                │
│  كل Application تُغلَّف في Software Package:                  │
│  ← الـ binary (الملف القابل للتنفيذ)                         │
│  ← Execution Manifest                                         │
│  ← Service Instance Manifest                                  │
│  ← ملفات الإعداد والمكتبات                                   │
│  ← التوقيع الرقمي (ara::crypto)                              │
│                                                                │
│  الناتج: .swpkg (Software Package)                           │
└──────────────────────────────┬─────────────────────────────────┘
                               │
                               ▼
┌────────────────────────────────────────────────────────────────┐
│  4. Testing & Validation (الاختبار)                            │
│                                                                │
│  ← Unit Tests على المطوّر حاسب                                │
│  ← Integration Tests مع محاكاة الخدمات الأخرى               │
│  ← HIL Testing على عتاد حقيقي                                │
│  ← Functional Safety Analysis (لـ ASIL)                      │
└──────────────────────────────┬─────────────────────────────────┘
                               │
                               ▼
┌────────────────────────────────────────────────────────────────┐
│  5. OTA Distribution (التوزيع عبر الهواء)                    │
│                                                                │
│  Backend Server ← يحمل .swpkg الموقّعة                       │
│       │                                                        │
│       │  عبر 4G/5G                                            │
│       ▼                                                        │
│  السيارة: UCM (Update and Configuration Management)           │
│  ← يُنزّل في الخلفية                                          │
│  ← يتحقق من التوقيع                                          │
│  ← يُثبّت عند إيقاف السيارة                                 │
└──────────────────────────────┬─────────────────────────────────┘
                               │
                               ▼
┌────────────────────────────────────────────────────────────────┐
│  6. Execution (التشغيل)                                        │
│                                                                │
│  Execution Manager:                                            │
│  ← يقرأ Machine Manifest لمعرفة Function Groups              │
│  ← يقرأ Execution Manifests لمعرفة التبعيات                  │
│  ← يُشغّل Processes بالترتيب الصحيح                          │
│  ← يراقب PHM للصحة المستمرة                                  │
│                                                                │
│  التطبيق يعمل الآن في السيارة.                                │
└────────────────────────────────────────────────────────────────┘
```

---

### نقطة مهمة: A/B Partitioning

كيف يضمن Rollback العودة للإصدار السابق بأمان؟

```
القرص (eMMC / SSD) مُقسَّم لنصفين:

Partition A: الإصدار الحالي (يعمل الآن)
Partition B: فارغة أو إصدار قديم

عند التحديث:
← حزمة جديدة تُكتب في Partition B
← عند الإقلاع: يُقلع من Partition B
← إذا نجح كل شيء: B أصبحت "الحالي"، A للتحديث القادم
← إذا فشل: يُعيد الإقلاع من Partition A

دائماً يوجد إصدار عامل للعودة إليه.
```

---


---

## الجزء السادس (أ): نظام متعدد الـ Processes — مثال كامل

### من الكاميرا إلى قرار القيادة

هذا المثال يوضّح كيف تتعاون Processes متعددة عبر ara::com.

---

### البنية الكاملة

```
┌─────────────────────────────────────────────────────────────────┐
│                     SoC (System on Chip)                        │
│                                                                 │
│  Process 1                 Process 2                           │
│  ┌──────────────────┐      ┌──────────────────┐                │
│  │  CameraService   │      │  RadarService    │                │
│  │                  │      │                  │                │
│  │ يقرأ كاميرا USB │      │ يقرأ Radar ADC   │                │
│  │ يُعالج الصورة   │      │ يُعالج الإشارة  │                │
│  │                  │      │                  │                │
│  │ ●CameraFeed Event│      │ ●RadarData Event │                │
│  └────────┬─────────┘      └────────┬─────────┘                │
│           │                         │                          │
│           │    SOME/IP / Shared Memory                         │
│           │                         │                          │
│           ▼                         ▼                          │
│  ┌─────────────────────────────────────┐                       │
│  │          FusionService              │                       │
│  │                                     │                       │
│  │ يستهلك: CameraFeed + RadarData     │                       │
│  │ يدمجهما: Sensor Fusion Algorithm   │                       │
│  │                                     │                       │
│  │ ●FusedObjects Event                │                       │
│  └──────────────────┬──────────────────┘                       │
│                     │                                          │
│                     │ SOME/IP                                  │
│                     │                                          │
│                     ▼                                          │
│  ┌──────────────────────────────────────┐                      │
│  │         PlanningService              │                      │
│  │                                      │                      │
│  │ يستهلك: FusedObjects                │                      │
│  │ يحسب: المسار والقرارات              │                      │
│  │                                      │                      │
│  │ ●DrivingCommands Method             │                      │
│  └──────────────────┬───────────────────┘                      │
│                     │                                          │
│                     │ CAN Gateway (إلى Classical ECUs)         │
│                     │                                          │
│    ┌────────────────┼────────────────┐                         │
│    ▼                ▼                ▼                         │
│  Engine ECU     Brake ECU      Steering ECU                    │
│  (Classical)    (Classical)    (Classical)                     │
└─────────────────────────────────────────────────────────────────┘
```

---

### الكود: FusionService الكامل

```cpp
// fusion_service.cpp
#include "ara/com/sample/camera_proxy.h"
#include "ara/com/sample/radar_proxy.h"
#include "ara/com/sample/fusion_skeleton.h"
#include "ara/exec/execution_client.h"
#include "ara/log/logger.h"

class FusionService : public ara::com::sample::FusionSkeleton {
    std::shared_ptr<CameraProxy> cameraProxy_;
    std::shared_ptr<RadarProxy>  radarProxy_;
    ara::log::Logger logger_;
    
    // آخر بيانات مستقبَلة
    std::optional<CameraFrame> lastCameraFrame_;
    std::optional<RadarData>   lastRadarData_;

public:
    FusionService(ara::core::InstanceSpecifier spec)
        : FusionSkeleton(spec)
        , logger_{ara::log::CreateLogger("FUSE", "Fusion Service")} {}

    void Initialize() {
        // ابحث عن خدمة الكاميرا
        CameraProxy::StartFindService(
            [this](auto handles, auto) {
                if (!handles.empty()) {
                    cameraProxy_ = std::make_shared<CameraProxy>(handles[0]);
                    cameraProxy_->CameraFeedEvent.Subscribe(5);
                    cameraProxy_->CameraFeedEvent.SetReceiveHandler(
                        [this]() { OnCameraFrame(); }
                    );
                    logger_.LogInfo() << "تم الاتصال بخدمة الكاميرا";
                }
            },
            ara::core::InstanceSpecifier{"/sensors/camera/front"}
        );

        // ابحث عن خدمة الرادار
        RadarProxy::StartFindService(
            [this](auto handles, auto) {
                if (!handles.empty()) {
                    radarProxy_ = std::make_shared<RadarProxy>(handles[0]);
                    radarProxy_->RadarDataEvent.Subscribe(5);
                    radarProxy_->RadarDataEvent.SetReceiveHandler(
                        [this]() { OnRadarData(); }
                    );
                    logger_.LogInfo() << "تم الاتصال بخدمة الرادار";
                }
            },
            ara::core::InstanceSpecifier{"/sensors/radar/front"}
        );

        // أعلن جاهزية الخدمة للـ Execution Manager
        ara::exec::ExecutionClient{}.ReportExecutionState(
            ara::exec::ExecutionState::kRunning
        );

        // أعلن عن هذه الخدمة على الشبكة
        this->OfferService();
    }

private:
    void OnCameraFrame() {
        auto samples = cameraProxy_->CameraFeedEvent.GetNewSamples();
        for (auto& s : samples) {
            lastCameraFrame_ = *s;
        }
        TryFuse();
    }

    void OnRadarData() {
        auto samples = radarProxy_->RadarDataEvent.GetNewSamples();
        for (auto& s : samples) {
            lastRadarData_ = *s;
        }
        TryFuse();
    }

    void TryFuse() {
        if (!lastCameraFrame_ || !lastRadarData_) return;

        // خوارزمية الدمج
        FusedObjects result = performFusion(*lastCameraFrame_, *lastRadarData_);

        // إرسال النتيجة لـ PlanningService
        FusedObjectsEvent.Send(result);

        logger_.LogDebug() << "تم دمج البيانات: " << result.objectCount << " جسم";
    }
};

int main() {
    FusionService service{ara::core::InstanceSpecifier{"/fusion/main"}};
    service.Initialize();

    // حلقة التشغيل الرئيسية
    while (true) {
        std::this_thread::sleep_for(std::chrono::milliseconds{1});
    }

    return 0;
}
```

---

### نقطة حرجة: Thread Safety في الخدمات

لاحظ أن `OnCameraFrame` و`OnRadarData` قد يُستدعيان من Threads مختلفة.

في الأنظمة الحقيقية:

```cpp
// يجب حماية البيانات المشتركة
std::mutex dataMutex_;

void OnCameraFrame() {
    std::lock_guard<std::mutex> lock{dataMutex_};
    // آمن للوصول الآن
    lastCameraFrame_ = ...;
    TryFuse();
}

void OnRadarData() {
    std::lock_guard<std::mutex> lock{dataMutex_};
    lastRadarData_ = ...;
    TryFuse();
}
```

أو استخدام Queue لفصل استقبال البيانات عن معالجتها.

---


---

## الجزء التاسع: التطوير العملي

### الفرق في بيئة التطوير

**تطوير Classical AUTOSAR:**

```
الأدوات:
← Vector DaVinci (أكثرها شيوعاً)
← ETAS ISOLAR
← EB tresos

اللغة: C (مُقيَّد جداً، MISRA C)
المحاكاة: SIL/HIL بأجهزة خاصة
الاختبار: باهظ التكلفة ومعقد
```

**تطوير Adaptive AUTOSAR:**

```
الأدوات:
← Vector MICROSAR Adaptive
← ETAS ECUREX Adaptive
← OpenAA (مفتوح المصدر)
← Eclipse Cyclone DDS (للتطوير السريع)

اللغة: C++14/17 مع مكتبات ara::
المحاكاة: على Linux العادي! (بدون عتاد خاص)
الاختبار: unit tests عادية + Docker
```

هذا الفرق الأخير ضخم جداً:

```
يمكن لمهندس C++ عادي أن يُطوّر Adaptive Application
على حاسبه الشخصي بـ Linux
دون أن يلمس عتاد السيارة.

في Classical: مستحيل بدون عتاد محدد.
```

---

### بنية المشروع النموذجية

```
adaptive_radar_service/
│
├── design/
│   ├── radar_service.arxml    ← وصف الخدمة (لا يزال XML في Adaptive)
│   └── deployment.arxml       ← إعدادات النشر
│
├── generated/
│   ├── radar_skeleton.h       ← مُولَّد تلقائياً من الـ arxml
│   └── radar_proxy.h          ← مُولَّد تلقائياً
│
├── src/
│   ├── radar_service.cpp      ← الكود الذي يكتبه المهندس
│   └── radar_algorithm.cpp    ← منطق معالجة الرادار
│
├── test/
│   ├── unit_tests.cpp         ← اختبارات الوحدة
│   └── integration_tests.cpp  ← اختبارات التكامل
│
├── CMakeLists.txt             ← بناء المشروع (نعم، CMake عادي)
└── manifest.json              ← إعدادات تشغيل التطبيق
```

---

### Application Manifest

هذا ما يُخبر Execution Manager بكيفية تشغيل التطبيق:

```json
{
  "applicationName": "RadarService",
  "version": "2.1.0",
  
  "startupConfig": {
    "startupOptions": ["--config", "/etc/radar/config.json"],
    "schedulingPolicy": "FIFO",
    "schedulingPriority": 80
  },
  
  "resourceGroups": [
    {
      "name": "RadarServiceGroup",
      "cpuCores": [2, 3],
      "memoryLimit": "512MB"
    }
  ],
  
  "dependencies": [
    "CameraService",
    "NetworkManagement"
  ]
}
```

هذا الملف يُقرأ في وقت التشغيل، مما يعني:

```
يمكن تغيير إعدادات التشغيل بدون إعادة ترجمة الكود.
تعديل الـ manifest كافٍ.
```

---

### خطوات تطوير Adaptive Application

```
الخطوة 1: تصميم الخدمة (Service Design)
← حدد اسم الخدمة وversion وInstance
← حدد الـ Methods والـ Events والـ Fields
← اكتب كل هذا في ملف .arxml

الخطوة 2: توليد الكود
← أداة التوليد تُنتج Skeleton وProxy
← نفس مبدأ Classical لكن بـ C++

الخطوة 3: تطوير منطق الخدمة
← اكتب كلاسك الذي يرث من الـ Skeleton
← نفّذ الـ Methods واملأ الـ Events

الخطوة 4: كتابة الـ Manifest
← أخبر Execution Manager بمتطلبات تطبيقك

الخطوة 5: الاختبار المحلي
← شغّل على Linux العادي
← استخدم محاكاة للخدمات الأخرى

الخطوة 6: الاندماج
← دمج مع بقية الخدمات على الـ SoC الحقيقي
← اختبار شامل
```

---

## الجزء العاشر: مقارنة شاملة Classic vs Adaptive

### جدول المقارنة الكامل

```
┌─────────────────────────────────────────────────────────────────────┐
│                    جانب المقارنة                                    │
├──────────────────────┬─────────────────────┬────────────────────────┤
│  الجانب              │  Classical AUTOSAR  │  Adaptive AUTOSAR      │
├──────────────────────┼─────────────────────┼────────────────────────┤
│ العتاد               │ MCU بسيط            │ SoC قوي                │
│ ذاكرة RAM            │ KB إلى MB           │ GB                     │
│ نظام التشغيل         │ OSEK OS             │ POSIX (Linux/QNX)      │
│ لغة البرمجة          │ C                   │ C++14/17               │
│ الجدولة              │ ثابتة               │ ديناميكية              │
│ الوحدة الأساسية      │ SWC (مكوّن)         │ Adaptive Application   │
│ الاتصال              │ Signal عبر RTE      │ Service عبر SOME/IP    │
│ شبكة الاتصال         │ CAN / LIN           │ Automotive Ethernet    │
│ تطبيق SOA            │ لا                  │ نعم، أساسي             │
│ اكتشاف الخدمات       │ ثابت                │ ديناميكي (SD)          │
│ التحديث              │ Flash جزئي          │ OTA كامل               │
│ معزول في الذاكرة؟    │ لا                  │ نعم (Process Isolation)│
│ ملائم لـ ASIL D؟     │ نعم بسهولة          │ بصعوبة، يحتاج جهداً   │
│ سرعة التطوير         │ بطيء ومعقد          │ أسرع، أدوات مألوفة     │
│ المحاكاة             │ تحتاج عتاداً        │ على Linux العادي       │
│ الاستخدام الأنسب     │ أنظمة التحكم الحرجة │ ADAS، شاشات، IoT      │
│ معيار الإصدار        │ R4.3 (مستقر)        │ R22-11, R23-11         │
└──────────────────────┴─────────────────────┴────────────────────────┘
```

---

### السيارة الحديثة: كلاهما معاً

هذه هي الصورة الحقيقية لسيارة 2024:

```
┌────────────────────────────────────────────────────────────────────┐
│                         السيارة                                    │
│                                                                    │
│  ┌────────────────────────────────┐                                │
│  │    High-Performance Domain     │                                │
│  │    Controller (HPDC)           │                                │
│  │                                │                                │
│  │  ┌──────────────────────────┐  │                                │
│  │  │   Adaptive AUTOSAR       │  │                                │
│  │  │   (QNX + ARA stack)      │  │                                │
│  │  │                          │  │                                │
│  │  │ • Camera Processing      │  │                                │
│  │  │ • Radar Fusion           │  │                                │
│  │  │ • ADAS Planning          │  │                                │
│  │  │ • OTA Management         │  │                                │
│  │  │ • Infotainment           │  │                                │
│  │  └──────────────────────────┘  │                                │
│  └─────────────────┬──────────────┘                                │
│                    │ Automotive Ethernet + CAN Gateway             │
│        ┌───────────┼────────────┐                                  │
│        │           │            │                                  │
│  ┌─────┴──┐  ┌─────┴──┐  ┌─────┴──┐                               │
│  │ Engine │  │ Brake  │  │Steering│                               │
│  │  ECU   │  │  ECU   │  │  ECU   │                               │
│  │        │  │        │  │        │                               │
│  │Classic │  │Classic │  │Classic │                               │
│  │AUTOSAR │  │AUTOSAR │  │AUTOSAR │                               │
│  │ASIL D  │  │ASIL D  │  │ASIL D  │                               │
│  └────────┘  └────────┘  └────────┘                               │
│                    │                                               │
│                CAN Bus                                             │
└────────────────────────────────────────────────────────────────────┘
```

---

## الجزء الحادي عشر: مسرد المفاهيم الجديدة

### مقارنة المصطلحات

```
┌────────────────────────────────────────────────────────────────┐
│     Classical AUTOSAR       →      Adaptive AUTOSAR            │
├─────────────────────────────┬──────────────────────────────────┤
│ SWC                         │ Adaptive Application             │
│ RTE                         │ ARA (ara::com)                   │
│ CAN Signal                  │ SOME/IP Service                  │
│ P-Port / R-Port             │ Skeleton / Proxy                 │
│ Sender-Receiver Interface   │ Event / Field                    │
│ Client-Server Interface     │ Method                           │
│ DCM + DEM                   │ ara::diag                        │
│ NvM                         │ ara::per (Persistency)           │
│ EcuM (حالات ECU)            │ State Management                 │
│ OS Task                     │ Process (مستقل في الذاكرة)       │
│ DET                         │ ara::log                         │
│ BSW Configuration Tools     │ CMake + JSON Manifest            │
│ Flash Programming           │ UCM + OTA                        │
│ WdgM                        │ Platform Health Management (PHM) │
│ E2E Protection              │ SOME/IP-E2E                      │
└─────────────────────────────┴──────────────────────────────────┘
```

---

### المسرد الشامل

```
┌────────────────────────────────────────────────────────────────────┐
│                   مصطلحات Adaptive AUTOSAR                         │
├─────────────────────────────────┬──────────────────────────────────┤
│ المصطلح                         │ المعنى                           │
├─────────────────────────────────┼──────────────────────────────────┤
│ Adaptive AUTOSAR / AP           │ النسخة التكيّفية لمعيار AUTOSAR  │
│ Classical AUTOSAR / CP          │ النسخة الكلاسيكية                │
│ POSIX                           │ معيار نظام التشغيل المحمول       │
│ SoC                             │ نظام على شريحة                  │
│ HPDC                            │ وحدة التحكم عالية الأداء         │
│ ARA                             │ واجهة برمجة Adaptive              │
│ ara::com                        │ واجهة الاتصال (Proxy/Skeleton)   │
│ ara::exec                       │ إدارة التنفيذ                    │
│ ara::diag                       │ إدارة التشخيص                    │
│ ara::per                        │ التخزين الدائم (Persistency)     │
│ ara::log                        │ التسجيل                          │
│ ara::crypto                     │ التشفير والأمان                  │
│ SOME/IP                         │ بروتوكول الاتصال الرئيسي         │
│ SOME/IP-SD                      │ اكتشاف الخدمات                   │
│ SOME/IP-E2E                     │ حماية البيانات                   │
│ SOA                             │ معمارية موجّهة بالخدمات          │
│ Service Provider                │ مُقدّم الخدمة                     │
│ Service Consumer                │ مستهلك الخدمة                    │
│ Skeleton                        │ واجهة جانب المُقدّم               │
│ Proxy                           │ واجهة جانب المستهلك             │
│ Method                          │ طلب/رد (مثل استدعاء دالة)       │
│ Event                           │ بث بيانات بدون طلب              │
│ Field                           │ قيمة قابلة للقراءة والتغيير     │
│ Execution Manager               │ مدير تشغيل التطبيقات            │
│ Machine State                   │ حالة الجهاز (Running, Update...) │
│ Application Manifest            │ إعدادات تشغيل التطبيق           │
│ UCM                             │ مدير التحديث والإعداد            │
│ OTA                             │ التحديث عبر الهواء              │
│ Rollback                        │ العودة للإصدار السابق            │
│ PHM                             │ إدارة صحة المنصة                │
│ State Management                │ إدارة الحالة                     │
│ Automotive Ethernet             │ إيثرنت السيارات                  │
│ 100BASE-T1 / 1000BASE-T1        │ معايير Ethernet في السيارات      │
│ ADAS                            │ أنظمة مساعدة السائق المتقدمة    │
│ Lidar                           │ ليزر قياس المسافة ثلاثي الأبعاد │
│ Radar                           │ رادار كشف الأجسام                │
│ USS                             │ حساسات موجات فوق صوتية          │
│ Sensor Fusion                   │ دمج بيانات الحساسات              │
│ SAE Level                       │ مستوى القيادة الذاتية            │
│ GPU                             │ وحدة معالجة الرسوميات           │
│ TOPS                            │ تريليون عملية في الثانية         │
│ Process Isolation               │ عزل العمليات في الذاكرة         │
│ Dynamic Linking                 │ تحميل المكتبات أثناء التشغيل    │
│ Digital Signing                 │ التوقيع الرقمي لحزم OTA         │
│ QNX                             │ نظام تشغيل POSIX حتمي للسيارات  │
│ AGL                             │ Automotive Grade Linux            │
│ MISRA C++                       │ معيار ترميز C++ للسيارات         │
│ ara::core::Result               │ حاوية النجاح أو الفشل بلا استثناء│
│ ara::core::Future               │ نتيجة عملية لامتزامنة            │
│ ara::core::Promise              │ مصدر نتيجة عملية لامتزامنة       │
│ ara::core::ErrorCode            │ رمز الخطأ مع نطاقه               │
│ ara::core::ErrorDomain          │ تصنيف نطاق الأخطاء               │
│ ara::core::InstanceSpecifier    │ معرّف النسخة في Manifest          │
│ SOME/IP-SD                      │ اكتشاف الخدمات ديناميكياً        │
│ OfferService                    │ إعلان الخدمة على الشبكة          │
│ StopOfferService                │ سحب الإعلان عن الخدمة            │
│ FindService                     │ البحث عن خدمة بمعرّفها           │
│ StartFindService                │ مراقبة توفر خدمة باستمرار        │
│ EventGroup                      │ مجموعة Events داخل خدمة واحدة   │
│ SubscribeEventgroup             │ الاشتراك في مجموعة أحداث         │
│ TTL                             │ وقت صلاحية الإعلان عن الخدمة    │
│ Re-offer                        │ تجديد إعلان الخدمة دورياً        │
│ Function Group                  │ مجموعة تطبيقات تعمل معاً         │
│ Function Group State            │ حالة مجموعة التطبيقات            │
│ Machine Manifest                │ إعداد الجهاز/الـ SoC كاملاً      │
│ Execution Manifest              │ إعداد تطبيق محدد                 │
│ Service Instance Manifest       │ عناوين الشبكة للخدمة             │
│ Service Interface Manifest      │ تعريف منطق الخدمة                │
│ Process State                   │ حالة العملية (Running/Terminated) │
│ Startup Dependencies            │ تبعيات الإقلاع بين التطبيقات    │
│ ReportExecutionState            │ إعلان التطبيق جاهزيته للـ EM    │
│ A/B Partitioning                │ تقسيم التخزين للتحديث الآمن      │
│ Shared Memory                   │ ذاكرة مشتركة بين Processes       │
│ Zero-Copy                       │ نقل البيانات بلا نسخ             │
│ Loaned Samples                  │ عينات مُعارة في Shared Memory    │
│ Huge Pages                      │ صفحات ذاكرة كبيرة لتحسين الأداء │
│ TLB                             │ مخزن ترجمة عناوين الذاكرة        │
│ DDS                             │ خدمة توزيع البيانات (بديل SOME/IP)│
│ CDR                             │ تمثيل البيانات المشترك في DDS    │
│ QoS                             │ سياسات جودة الخدمة في DDS        │
│ V2X                             │ تواصل السيارة مع كل شيء حولها   │
│ swpkg                           │ حزمة Software Package للنشر      │
│ UDP Multicast                   │ بث UDP لمجموعة مستقبلين          │
│ PHM                             │ إدارة صحة المنصة                │
│ Alive Supervision               │ إشراف الحياة (checkpoint دوري)  │
│ Deadline Supervision            │ إشراف الميعاد (ضمن نطاق زمني)  │
│ Logical Supervision             │ إشراف منطقي (تسلسل صحيح)       │
│ Supervised Entity               │ الكيان الخاضع للإشراف           │
│ CheckpointId                    │ معرّف نقطة التحقق               │
│ Recovery Action                 │ إجراء الاسترداد عند الخطأ       │
│ Freedom from Interference       │ الحرية من التداخل بين ASILs     │
│ Mixed-Criticality System        │ نظام بمستويات ASIL متعددة       │
│ CPU Partitioning                │ تخصيص نوى CPU لمستويات ASIL     │
└─────────────────────────────────┴──────────────────────────────────┘
```

---

## الجزء الثاني عشر: أسئلة المقابلات

### الأسئلة الأكثر شيوعاً

**1. ما الفرق الجوهري بين Classical وAdaptive AUTOSAR؟**

```
الجواب الذي يُميّزك:

لا تقل فقط "CP يستخدم C وAP يستخدم C++"

قل:
"الفرق الجوهري في نموذج الاتصال وديناميكية النظام.
Classical يعتمد على Signals ثابتة معروفة وقت التصميم.
Adaptive يعتمد على Services تُكتشف ديناميكياً أثناء التشغيل.
هذا يُمكّن OTA والتوسع بخدمات جديدة بدون إعادة تصميم كامل."
```

**2. ما هو SOME/IP ولماذا لا يكفي CAN في Adaptive؟**

```
CAN له حد أقصى 8 bytes (64 في CAN-FD) وسرعة 1 Mbps.
كاميرا 4K تُنتج 360 MB/s.
الفجوة لا تُحل بـ CAN أبداً.

SOME/IP هو بروتوكول فوق Automotive Ethernet (حتى 10 Gbps)
يُضيف: اكتشاف الخدمات، توجيه الطلبات، اشتراكات الأحداث.
يُحوّل شبكة السيارة من شبكة بيانات إلى شبكة خدمات.
```

**3. ما هو الفرق بين Proxy وSkeleton في ara::com؟**

```
Skeleton: ما يبني عليه مُقدّم الخدمة
← يُعلن عن الخدمة على الشبكة
← يُعرّف تنفيذ الـ Methods والـ Events

Proxy: ما يستخدمه مستهلك الخدمة
← يبحث عن الخدمة ويتصل بها
← يستدعي الـ Methods ويشترك في الـ Events
← يُخفي تفاصيل SOME/IP عن المطوّر
```

**4. كيف يعمل OTA في Adaptive AUTOSAR؟**

```
UCM (Update and Configuration Management) يُدير العملية:

1. تنزيل الحزمة في الخلفية (السيارة تعمل)
2. التحقق بالتوقيع الرقمي (ara::crypto)
3. تثبيت الحزمة بعد إيقاف السيارة
4. تفعيل الإصدار الجديد عند الإقلاع
5. التحقق من سلامة النظام
6. إذا فشل: Rollback تلقائي للإصدار السابق
```

**5. لماذا يصعب تحقيق ASIL D في Adaptive؟**

```
ASIL D يتطلب إثبات تحديدية النظام وعدم وجود حالات غير متوقعة.

Adaptive بطبيعته:
← يشغّل Processes ديناميكياً
← OTA يُغيّر سلوكه باستمرار
← نظام POSIX نفسه معقد ويصعب إثباته بالكامل

الحل العملي: الوظائف ASIL D تبقى في Classical.
Adaptive يمكنه دعم ASIL مختلفة مع جهد تحقق إضافي.
ASIL D الخالص يبقى أسهل في Classical.
```

**6. ما هو PHM والفرق بين أنواع الإشراف الثلاثة؟**

```
PHM = Platform Health Management

هو WdgM الـ Adaptive لكن بثلاثة مستويات إشراف:

1. Alive Supervision:
   "هل التطبيق لا يزال يعمل ويُرسل checkpoints بشكل دوري؟"
   → يكشف: التجمّد الكامل أو الحلقات اللانهائية

2. Deadline Supervision:
   "هل انتهى من مهمته في الوقت المحدد (بين حد أدنى وأقصى)؟"
   → يكشف: البطء غير الطبيعي أو الإسراع غير المتوقع

3. Logical Supervision:
   "هل تسلسل العمليات منطقي وصحيح؟"
   → يكشف: تخطي خطوات حرجة أو تنفيذها بترتيب خاطئ

عند اكتشاف مشكلة، Recovery Action متدرجة:
← أولاً: إعادة تشغيل الـ Process المشكوك فيها
← ثانياً: تغيير Function Group State
← أخيراً: إيقاف الـ SoC (إذا كان الخطأ حرجاً للسلامة)
```

**7. ما الفرق بين Method وEvent وField في SOME/IP؟**

```
Method  ← طلب + رد (مثل استدعاء دالة)
         مثال: "احسب لي أقصر مسار"

Event   ← بث بدون طلب (أحادي الاتجاه)
         مثال: "كل 50ms أبعث إطار الكاميرا"

Field   ← قيمة لها حالة، قابلة للقراءة والتغيير والإشعار
         مثال: حالة النظام (Running/Idle/Error)
```

**8. كيف تُفرّق بين متى تستخدم Classical ومتى تستخدم Adaptive؟**

```
استخدم Classical إذا:
← الوظيفة تؤثر مباشرة على سلامة السيارة (ASIL D خالص)
← تحتاج حتمية مضمونة بالميلي ثانية
← موارد العتاد محدودة
← مثال: ABS، ESP، حقن الوقود

استخدم Adaptive إذا:
← تحتاج معالجة بيانات ضخمة
← تحتاج تحديثات OTA
← تتعامل مع خوارزميات ذكاء اصطناعي
← تحتاج اتصالاً بالإنترنت أو السحابة
← مثال: كاميرات ADAS، شاشة المعلومات، الملاحة
```

**9. ما هو ara::core::Result ولماذا نستخدمه بدلاً من الاستثناءات؟**

```
في أنظمة AUTOSAR الحرجة، الاستثناءات ممنوعة لأنها:
← تُسبّب وقت تنفيذ غير متوقع (تكسر الحتمية)
← تُعقّد التحقق الرسمي لـ ASIL
← Stack unwinding قد يُسبّب مشاكل في الأنظمة المدمجة

ara::core::Result<T, E> بديل آمن:
← إما نجاح (T = القيمة)
← أو فشل (E = كود الخطأ)
← يُجبر المهندس على التعامل الصريح مع كلا الحالتين
← وقت تنفيذ محدد ومضمون
```

**10. ما الفرق بين Function Group وMachine State في Adaptive؟**

```
Machine State: حالة الجهاز كله
← Running, Startup, Shutdown, Update
← يُعبّر عن الحالة العامة للـ SoC

Function Group: مجموعة Applications تعمل معاً
← كل Function Group لها حالاتها الخاصة
← مثال: DrivingMode له حالات Normal, Highway, Parking
← تغيير حالة Function Group يُشغّل/يوقف Applications محددة
← أكثر مرونة من Machine State لأن Function Groups متعددة تعمل في آنٍ واحد
```

**11. متى تستخدم Shared Memory بدلاً من SOME/IP لنقل البيانات؟**

```
استخدم Shared Memory عندما:
← البيانات كبيرة (إطارات الكاميرا، Lidar point cloud)
← الـ Processes على نفس الـ SoC
← كل نسخة إضافية تهدر موارد ثمينة

الـ SOME/IP (Zero-Copy) يدعم هذا عبر Loaned Samples:
← Skeleton يكتب مباشرة في Shared Memory
← Proxy يقرأ من نفس المنطقة
← لا نسخ وسيطة على الإطلاق

لا تستخدم Shared Memory عبر شبكة خارجية (ECUs مختلفة)
← هناك لا مفر من SOME/IP عبر Ethernet
```

**12. ما الأنواع الأربعة لملفات Manifest في Adaptive وما دور كل منها؟**

```
Machine Manifest:
← إعداد الجهاز كله (SoC)
← الشبكات، Function Groups، الصلاحيات

Execution Manifest:
← إعداد Application محددة
← الـ binary، التبعيات، الـ CPU والذاكرة

Service Instance Manifest:
← عناوين الشبكة للخدمة
← بروتوكول TCP/UDP، الـ Port

Service Interface Manifest:
← تعريف المنطق: Methods، Events، Fields
← أنواع البيانات وإصدار الواجهة
```

---

## الجزء الثالث عشر: خريطة الطريق للمهندس

### مسار التعلم الموصى به

إذا كنت قادماً من عالم Classical AUTOSAR:

```
الأسبوع 1-2: الأساسيات
□ C++11/14/17 (خاصة: smart pointers, futures, lambdas)
□ فهم POSIX وLinux processes وthreads
□ مفاهيم SOA بشكل عام

الأسبوع 3-4: Adaptive
□ اقرأ AUTOSAR Adaptive Specification (مجاناً على autosar.org)
□ ركّز على: ara::com وara::exec أولاً
□ جرّب بيئة تطوير مثل OpenAA

الأسبوع 5-6: التطبيق
□ ابنِ Adaptive Application بسيطاً
□ بالتشغيل على Linux
□ جرّب SOME/IP بأداة مثل vsomeip

الأسبوع 7-8: التعمق
□ SOME/IP Specification
□ Automotive Ethernet وأساسيات TCP/IP
□ ISO 26262 وكيف يتقاطع مع Adaptive
```

إذا كنت قادماً من عالم Software العام:

```
ابدأ من هنا:
□ Classical AUTOSAR أساسياته (الـ SWC وRTE وBSW)
← لفهم المشكلة التي حلّها Adaptive

ثم:
□ نفس المسار السابق لكن بوتيرة أبطأ
□ ركّز على AUTOSAR arxml وتصميم الخدمات
```

---

### المشاريع التدريبية

```
المشروع الأول: Temperature Monitor Service
← خدمة بسيطة تُعلن Event لدرجة الحرارة كل ثانية
← مستهلك يستقبل ويطبع
← التشغيل على Linux المحلي
الهدف: فهم Skeleton / Proxy / Event

المشروع الثاني: Calculator Service
← خدمة تُقدّم Method للحساب
← مستهلك يستدعي ويستقبل النتيجة
الهدف: فهم Methods وRequest/Response

المشروع الثالث: Vehicle Status Service
← Field يُمثّل حالة السيارة
← يمكن Get/Set/Subscribe
الهدف: فهم Fields وNotifications

المشروع الرابع: Multi-Service System
← ثلاث خدمات تتعاون عبر SOME/IP-SD
← Service Discovery في العمل
الهدف: فهم النظام الكامل
```

---

## الجزء الرابع عشر: Cheat Sheet للمراجعة

### كل ما تحتاجه في صفحتين

```
Adaptive AUTOSAR = AUTOSAR لأنظمة السيارات الحديثة والمتصلة

متى تُستخدم؟
← ADAS (كاميرات، رادار، ليدار)
← السيارات ذاتية القيادة
← الشاشات والملاحة والترفيه
← أي وظيفة تحتاج OTA أو اتصال بالإنترنت

على ماذا تعمل؟
← SoC قوي (مثل NVIDIA Orin)
← POSIX OS (Linux أو QNX)
← C++14/17

الوحدة الأساسية:
Adaptive Application ← Process مستقل
يُقدّم أو يستهلك Service

الاتصال:
SOME/IP فوق Automotive Ethernet
├── Method   = طلب + رد
├── Event    = بث دوري
└── Field    = قيمة ذات حالة

اكتشاف الخدمات:
SOME/IP-SD ← تلقائي وديناميكي
OfferService → StopOfferService → FindService → StartFindService
TTL ← صلاحية الإعلان (يُجدَّد قبل انتهائه)

ARA (واجهة البرمجة):
ara::core   ← Result, Future, Promise, ErrorCode, InstanceSpecifier
ara::com    ← Proxy / Skeleton
ara::exec   ← إدارة التطبيقات وFunction Groups
ara::diag   ← التشخيص
ara::per    ← التخزين الدائم
ara::log    ← التسجيل
ara::crypto ← التشفير والأمان

دورة حياة التطبيق:
Execution Manifest ← يُعرّف Process وتبعياتها ومواردها
Function Group ← مجموعة Apps تعمل في حالة معينة
Process States: Idle → Running → Terminating → Terminated
ReportExecutionState(kRunning) ← إعلان الجاهزية للـ EM

ملفات Manifest (الأربعة):
Machine Manifest      ← الجهاز كله
Execution Manifest    ← التطبيق
Service Instance      ← عناوين الشبكة
Service Interface     ← تعريف المنطق

الذاكرة والأداء:
Shared Memory ← للبيانات الكبيرة (كاميرات، Lidar)
Zero-Copy / Loaned Samples ← بلا نسخ وسيطة
A/B Partitioning ← يضمن Rollback آمن

مكدس الاتصال (من فوق لتحت):
Application → ara::com → CM → SOME/IP → TCP/UDP → IP → Eth Driver → PHY → الكابل

Events: UDP (لا يهم فقدان إطار)
Methods: TCP (يجب أن يصل)

DDS vs SOME/IP:
SOME/IP ← الأساس في AUTOSAR AP
DDS ← قادم من Robotics، QoS أغنى، مدعوم كـ binding بديل

التحديثات:
OTA عبر UCM
مع التوقيع الرقمي والـ Rollback التلقائي

الأمان:
Classical للوظائف ASIL D الخالصة
Adaptive يدعم ASIL مع جهد تحقق إضافي
PHM = WdgM الـ Adaptive (أكثر ذكاءً):
  Alive Supervision    ← هل لا يزال حياً؟
  Deadline Supervision ← هل أنجز في الوقت؟
  Logical Supervision  ← هل التسلسل صحيح؟
  Recovery: Process → Function Group → SoC (متدرج)
Freedom from Interference ← فصل الـ Processes حرجة عن بعضها

الفرق الأكبر عن Classical:
Classical: كل شيء ثابت ومعروف مسبقاً
Adaptive: كل شيء ديناميكي وقابل للتغيير

الجملة للمقابلة:
"Adaptive AUTOSAR يُحوّل السيارة من نظام مُصمَّم مرة واحدة
إلى منصة برمجية تتطور باستمرار مثل هاتفك الذكي،
مع الحفاظ على متطلبات الأمان الصارمة لصناعة السيارات."
```

---

## الخاتمة

### وصلنا إلى النهاية

هذا الدليل قطع رحلة كاملة.

بدأنا بسؤال واحد:

```
"لماذا Classical AUTOSAR لا يكفي؟"
```

ووصلنا إلى فهم كامل لعالم مختلف تماماً:

```
من Signal بسيط على CAN
إلى Service موزّعة فوق Ethernet

من Task ثابت يعمل كل 10ms
إلى Process ديناميكي يبدأ وينتهي

من كود يُكتب مرة واحدة
إلى نظام يتطور بعد البيع عبر OTA

من Classical AUTOSAR
إلى Adaptive AUTOSAR
```

هذا التحول لم يكن ترفاً هندسياً.

كان ضرورة فرضتها الكاميرات والرادار والذكاء الاصطناعي وسيارات ذاتية القيادة.

---

ما تحمله من هذا الدليل ليس فقط مفاهيم.

هو طريقة تفكير في كيفية بناء أنظمة برمجية معقدة حقيقية.

سواء عملت يوماً على سيارة أو لم تعمل.

هذه المبادئ — الخدمات الموزعة، الاكتشاف الديناميكي، الأمان المتعدد الطبقات — موجودة في كل نظام كبير.

أنت الآن تفهمها.

**استخدمها.**

---

> *"أصعب ما في هندسة السيارات ليس حساب قوة الاحتكاك.*
> *أصعبه هو بناء برنامج يجب أن يعمل بلا أخطاء،*
> *ويتطور باستمرار، ولا يقتل أحداً.*
> *Adaptive AUTOSAR هو محاولة الصناعة للإجابة على هذا التحدي."*

