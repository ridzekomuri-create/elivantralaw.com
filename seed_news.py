"""Load the regulatory news articles into the database.
Safe to re-run: existing articles are updated by slug, new ones are inserted."""
from datetime import date

from app import app
from models import News, db

SEED_NEWS = [
    {
        "slug": "switzerland-transparency-register-2026",
        "published_at": date(2026, 10, 1),
        "service_slug": "registration",
        "source_name": "economiesuisse",
        "source_url": "https://www.economiesuisse.ch/en/articles/transparency-registry-new-obligations-companies-effective-october-1-2026",
        "title": "Швейцария запускает центральный реестр бенефициаров: что меняется для компаний с 1 октября 2026",
        "title_en": "Switzerland launches a central beneficial ownership register: what changes for companies from 1 October 2026",
        "excerpt": "С 1 октября 2026 года в Швейцарии действует закон о прозрачности юридических лиц. Компании должны установить своих бенефициаров и внести данные в центральный электронный реестр.",
        "excerpt_en": "From 1 October 2026 Switzerland's transparency law applies. Companies must identify their beneficial owners and record them in a central electronic register.",
        "content": (
            "С 1 октября 2026 года в Швейцарии вступил в силу Федеральный закон о прозрачности юридических лиц и идентификации бенефициарных владельцев (TJPG), а также изменения в законе о борьбе с отмыванием денег. Закон вводит центральный электронный реестр бенефициарных владельцев компаний.\n\n"
            "Под действие закона попадают акционерные общества, общества с ограниченной ответственностью, кооперативы и часть инвестиционных и коммандитных товариществ. Требования распространяются и на иностранные компании, если у них есть швейцарский филиал, фактическое управление в Швейцарии или недвижимость в стране. Исключения: публично торгуемые компании, пенсионные фонды и компании, большинство которых принадлежит государству.\n\n"
            "Компания обязана установить своих бенефициарных владельцев, проверить их личность и задокументировать сведения. Подача данных идёт в основном через платформу EasyGov.swiss; в перспективе возможна подача через кантональные торговые реестры.\n\n"
            "Что стоит сделать уже сейчас: проверить, попадает ли структура под закон; построить карту владения до конечного бенефициара; подготовить документы, подтверждающие личность владельцев; заранее зарегистрироваться на EasyGov.swiss. Сроки для уже существующих компаний лучше уточнять на официальном сайте реестра transpareg.admin.ch: в открытых обзорах закона конкретные сроки для действующих компаний не указаны.\n\n"
            "Для клиентов, которые открывают или обслуживают швейцарские структуры, это повод пересмотреть карту владения до того, как вопросы появятся у банка или регулятора."
        ),
        "content_en": (
            "From 1 October 2026 Switzerland's Federal Act on the Transparency of Legal Entities and the Identification of Beneficial Owners (TJPG) applies, together with amendments to the Anti-Money Laundering Act. The law introduces a central electronic register of companies' beneficial owners.\n\n"
            "The law covers stock corporations, limited liability companies, cooperatives and certain investment and limited partnerships. Foreign companies are covered if they have a Swiss branch, are actually managed from Switzerland, or own Swiss real estate. Exceptions include publicly traded companies, pension funds and companies majority-owned by the public sector.\n\n"
            "Companies must identify their beneficial owners, verify their identities and document the relevant information. Submissions are made mainly through the EasyGov.swiss platform, with cantonal commercial registries a possible future option.\n\n"
            "What to do now: check whether the structure falls within the law; map ownership down to the ultimate beneficial owner; prepare identity documents for the owners; register on EasyGov.swiss in advance. For deadlines that apply to existing companies, check the official register site transpareg.admin.ch: the public overviews we reviewed do not specify separate deadlines for existing companies.\n\n"
            "For clients who set up or run Swiss structures, this is a reason to review the ownership map before questions come from a bank or a regulator."
        ),
    },
    {
        "slug": "mica-transition-ended-2026",
        "published_at": date(2026, 7, 1),
        "service_slug": "blockchain",
        "source_name": "AMF (заявление ESMA об окончании переходного периода MiCA)",
        "source_url": "https://www.amf-france.org/en/news-publications/news/end-mica-transitional-period-esma-sets-out-its-expectations-professionals-and-warns-retail-investors",
        "title": "MiCA: переходный период закончился 1 июля 2026. Криптоуслуги в ЕС теперь требуют авторизации",
        "title_en": "MiCA: the transition period ended on 1 July 2026. Crypto services in the EU now require authorisation",
        "excerpt": "1 июля 2026 года закончился переходный период регламента MiCA. Предоставлять криптоуслуги в ЕС могут только компании с авторизацией, а работавшие без неё обязаны были свернуть деятельность.",
        "excerpt_en": "The MiCA transition period ended on 1 July 2026. Only authorised firms may provide crypto services in the EU; firms without authorisation had to wind down.",
        "content": (
            "1 июля 2026 года закончился переходный период действия регламента MiCA (Markets in Crypto-Assets). Теперь предоставлять криптоуслуги в ЕС могут только поставщики, получившие авторизацию как поставщики криптоуслуг (CASP). Национальные регистрации, которые действовали в переходный период, больше не дают такого права.\n\n"
            "Европейский регулятор ценных бумаг ESMA 17 апреля 2026 года подтвердил, что переходный период завершится окончательно и без продления. 23 июня 2026 года ESMA опубликовал заявление о том, как компании без разрешения должны сворачивать деятельность: план выхода должен был быть полностью выполнен к 1 июля, а клиентов нужно было вывести из сервиса упорядоченно и без необоснованного ущерба.\n\n"
            "Авторизованным компаниям ESMA рекомендовал заранее перенести существующих клиентов из ЕС на лицензированную базу. Для тех, кто работал по национальным регистрациям, это означает: без авторизации продолжать обслуживание клиентов в ЕС нельзя.\n\n"
            "Что мы делаем для клиентов: оцениваем, требуется ли авторизация для конкретной модели бизнеса; выбираем юрисдикцию лицензирования внутри ЕС с учётом сроков и требований; готовим комплаенс-пакет и подходы к взаимодействию с банками и платёжными провайдерами.\n\n"
            "Материал носит информационный характер и не является юридической консультацией."
        ),
        "content_en": (
            "On 1 July 2026 the transition period under the Markets in Crypto-Assets Regulation (MiCA) ended. From that date only providers authorised as crypto-asset service providers (CASPs) may offer crypto services in the EU. National registrations that were valid during the transition no longer allow this.\n\n"
            "On 17 April 2026 the European securities regulator ESMA confirmed that the transition period would end definitively, without extension. On 23 June 2026 ESMA published a statement on how unauthorised firms must wind down: their wind-down plans had to be fully implemented by 1 July, with clients offboarded in an orderly way and without undue harm.\n\n"
            "ESMA also expected authorised firms to onboard their existing EU clients before the transition ended. For firms that operated under national registrations, this means they cannot continue serving EU clients without authorisation.\n\n"
            "What we do for clients: assess whether a given business model requires authorisation; choose an EU licensing jurisdiction with timelines and requirements in mind; prepare the compliance package and the approach to banks and payment providers.\n\n"
            "This article is for information only and is not legal advice."
        ),
    },
    {
        "slug": "new-zealand-online-casino-regulations-2026",
        "published_at": date(2026, 7, 3),
        "service_slug": "gambling",
        "source_name": "Vixio",
        "source_url": "https://www.vixio.com/blog/gambling-regulatory-deadlines-to-watch-in-july-2026",
        "title": "Новая Зеландия вводит регулирование онлайн-казино: плата за заявку, сбор с прибыли и требования к игрокам",
        "title_en": "New Zealand introduces online casino regulation: application fee, profit levy and player requirements",
        "excerpt": "С 3 июля 2026 года действуют Регламенты 2026 года о регулировании онлайн-казино. Они задают порядок заявки на лицензию, сбор с прибыли операторов и правила защиты игроков.",
        "excerpt_en": "The Online Casino Gambling Regulations 2026 took effect on 3 July 2026. They set the licence application process, an operator profit levy and player protection rules.",
        "content": (
            "С 3 июля 2026 года в Новой Зеландии действуют Регламенты 2026 года о регулировании онлайн-казино. Они задают порядок получения лицензии и правила работы операторов на местном рынке.\n\n"
            "Заявка начинается с заявления о заинтересованности (expression of interest), за которое взимается плата NZ$19 000. Действующие операторы также будут платить сбор 3,5% от прибыли по онлайн-играм за каждый отчётный период.\n\n"
            "Регламенты охватывают несколько направлений. Профилактика игровой зависимости: лимиты и возможность самоисключения. Защита игроков: проверка личности по документам и запрет отдельных способов оплаты, в частности кредитных карт. Реклама и маркетинг: разрешённые каналы, возрастные требования, предупреждающие сообщения и ограничения содержания.\n\n"
            "Для операторов из этого следует практическая задача: платёжная инфраструктура, процедуры KYC и маркетинговые кампании должны соответствовать местным требованиям до подачи заявки, а не после.\n\n"
            "Наша роль: оцениваем готовность бизнеса к заявке, выстраиваем структуру операционной компании и платёжных потоков, сопровождаем диалог с регулятором. Материал носит информационный характер и не является юридической консультацией."
        ),
        "content_en": (
            "The Online Casino Gambling Regulations 2026 took effect in New Zealand on 3 July 2026. They set out how operators obtain a licence and how they may operate in the local market.\n\n"
            "An application starts with an expression of interest, which carries a NZ$19,000 fee. Operators will also pay a levy of 3.5% of their online gambling profits for each return period.\n\n"
            "The regulations cover several areas. Harm prevention: limits and self-exclusion options. Consumer protection: identity verification with ID documents and a ban on certain payment methods, including credit cards. Advertising and marketing: permitted channels, age requirements, warning messages and content restrictions.\n\n"
            "For operators, the practical task is that payment infrastructure, KYC procedures and marketing campaigns must meet local requirements before the application is filed, not after.\n\n"
            "Our role: we assess how ready a business is to apply, structure the operating company and payment flows, and support the dialogue with the regulator. This article is for information only and is not legal advice."
        ),
    },
    {
        "slug": "oecd-pillar-two-side-by-side-2026",
        "published_at": date(2026, 1, 5),
        "service_slug": "tax-legal",
        "source_name": "Holland & Knight",
        "source_url": "https://www.hklaw.com/en/insights/publications/2026/01/oecd-pillar-two-side-by-side-safe-harbor-package",
        "title": "OECD упростил Pillar Two: новые safe harbour для международных групп компаний",
        "title_en": "OECD simplifies Pillar Two: new safe harbours for international groups",
        "excerpt": "5 января 2026 года OECD опубликовал пакет Side-by-Side по глобальному минимальному налогу. Он вводит несколько safe harbour и облегчает правила для групп с американскими материнскими компаниями.",
        "excerpt_en": "On 5 January 2026 the OECD published its Side-by-Side package for the global minimum tax. It adds several safe harbours and eases the rules for groups with US parents.",
        "content": (
            "5 января 2026 года Инклюзивная структура OECD/G20, в которую входят 147 юрисдикций, опубликовала пакет Side-by-Side по правилам Pillar Two о глобальном минимальном налоге 15%.\n\n"
            "Пакет вводит несколько safe harbour. Side-by-Side safe harbour обнуляет доплату IIR и UTPR для подходящих групп. Safe harbour для материнской компании (UPE) обнуляет UTPR только в юрисдикции головной компании. Safe harbour для налоговых стимулов (SBTI) засчитывает квалифицированные льготы как уплаченные налоги в пределах ограничений по субстанции. Упрощённый safe harbour по эффективной ставке (ETR) обнуляет доплату, если ETR составляет не менее 15%.\n\n"
            "Сроки зависят от правила. SbS, UPE и SBTI применяются к финансовым годам, начинающимся с 1 января 2026 года. Упрощённый ETR safe harbour — к годам, начинающимся с 31 декабря 2026 года, с возможностью раннего применения с 31 декабря 2025 года. Переходный safe harbour по отчётности CbCR продлён на финансовые годы, заканчивающиеся 31 декабря 2027 года.\n\n"
            "Важная оговорка: на момент публикации в центральном реестре OECD только США признаны подходящими для Side-by-Side safe harbour. Остальные юрисдикции могут запросить оценку в 2027–2028 годах.\n\n"
            "Что это значит для групп компаний: проверить, какой safe harbour доступен для каждой юрисдикции группы и с какого финансового года; пересчитать эффективную ставку по каждой стране; учесть, что QDMTT остаётся основным механизмом защиты налоговой базы внутри стран.\n\n"
            "Материал носит информационный характер и не является налоговой консультацией."
        ),
        "content_en": (
            "On 5 January 2026 the OECD/G20 Inclusive Framework, comprising 147 jurisdictions, published the Side-by-Side package for the Pillar Two global minimum tax of 15%.\n\n"
            "The package introduces several safe harbours. The Side-by-Side safe harbour deems IIR and UTPR top-up taxes zero for eligible groups. The Ultimate Parent Entity (UPE) safe harbour deems UTPR liability zero only in the parent's own jurisdiction. The substance-based tax incentives (SBTI) safe harbour treats qualified incentives as taxes paid, subject to substance caps. The simplified effective tax rate (ETR) safe harbour deems the top-up zero where the ETR is at least 15%.\n\n"
            "Timing depends on the rule. The SbS, UPE and SBTI safe harbours apply to fiscal years beginning on or after 1 January 2026. The simplified ETR safe harbour applies to fiscal years beginning on or after 31 December 2026, with optional early application from 31 December 2025. The transitional CbCR safe harbour is extended to fiscal years ending on or before 31 December 2027.\n\n"
            "An important caveat: at publication, the OECD's central record listed only the United States as meeting the criteria for the Side-by-Side safe harbour. Other jurisdictions may request an assessment in 2027–2028.\n\n"
            "What this means for groups: check which safe harbour is available for each jurisdiction in the group and from which fiscal year; recalculate the effective tax rate country by country; remember that QDMTTs remain the main mechanism protecting each country's tax base.\n\n"
            "This article is for information only and is not tax advice."
        ),
    },
    {
        "slug": "eu-amlr-applies-july-2027",
        "published_at": date(2026, 7, 16),
        "service_slug": "banking",
        "source_name": "Fintech Global",
        "source_url": "https://fintech.global/2026/07/16/eu-amlr-why-firms-cant-wait-for-2027-to-prepare/",
        "title": "Единые AML-правила ЕС вступают в силу 10 июля 2027 года: почему готовиться нужно уже сейчас",
        "title_en": "The EU's single AML rulebook applies from 10 July 2027: why preparation should start now",
        "excerpt": "Регламент (ЕС) 2024/1624 (AMLR) станет прямо действующим во всех странах ЕС 10 июля 2027 года. Он заменит большую часть национальных правил ПОД/ФТ и ужесточит проверку клиентов.",
        "excerpt_en": "Regulation (EU) 2024/1624 (AMLR) applies directly across the EU from 10 July 2027. It replaces most national AML rules and tightens customer due diligence.",
        "content": (
            "Регламент (ЕС) 2024/1624, известный как AMLR, будет действовать напрямую во всех странах ЕС с 10 июля 2027 года. Впервые в ЕС появляется единый свод правил по борьбе с отмыванием денег, который не нужно переносить в национальное законодательство. Большая часть национальных норм при этом заменяется.\n\n"
            "Надзор берёт на себя новый орган — AMLA, Управление ЕС по борьбе с отмыванием денег и финансированием терроризма. Регламент задаёт более детальный базовый уровень проверки клиентов (CDD), который дополнят технические стандарты AMLA. Стандарты охватят объём информации и документов для стандартной, упрощённой и усиленной проверки, способы проверки личности физических и юридических лиц и бенефициаров, а также критерии для электронной идентификации и цифровой регистрации клиентов.\n\n"
            "Круг обязанных лиц расширяется. Регламент затрагивает торговцев дорогими товарами и компании за пределами ЕС, если у них есть филиалы или дочерние структуры в ЕС либо деловые отношения с организациями ЕС, которые обязаны соблюдать эти правила.\n\n"
            "Для клиентов, которые открывают счета в банках и платёжных провайдерах ЕС, это значит, что требования к документам о структуре владения и бенефициарах будут строже. Банки начнут применять новые стандарты заранее, поэтому ждать 2027 года не стоит.\n\n"
            "Что мы делаем: заранее проверяем структуру владения и источники средств; готовим пакет документов под требования банков и PSP; помогаем выстроить регулярную проверку клиентов, чтобы не терять счета при смене правил.\n\n"
            "Материал носит информационный характер и не является юридической консультацией."
        ),
        "content_en": (
            "Regulation (EU) 2024/1624, known as the AMLR, will apply directly in all EU Member States from 10 July 2027. For the first time the EU gets a single anti-money laundering rulebook that does not have to be transposed into national law. Most national rules are replaced.\n\n"
            "Supervision falls to a new body, AMLA, the EU Authority for anti-money laundering and countering the financing of terrorism. The regulation sets a more prescriptive baseline for customer due diligence (CDD), which AMLA's technical standards will complete. The standards cover the information and documents needed for standard, simplified and enhanced due diligence, how to verify individuals, legal entities and beneficial owners, and criteria for electronic identification and digital onboarding.\n\n"
            "The circle of obliged entities widens. It covers traders in high-value goods and non-EU companies that have EU branches or subsidiaries, or business relationships with EU obliged entities.\n\n"
            "For clients opening accounts with EU banks and payment providers, this means stricter requirements for documents on ownership structure and beneficial owners. Banks will start applying the new standards in advance, so waiting until 2027 is not advisable.\n\n"
            "What we do: review ownership structure and sources of funds in advance; prepare document packages for bank and PSP requirements; help set up regular client reviews so accounts are not lost when the rules change.\n\n"
            "This article is for information only and is not legal advice."
        ),
    },
    {
        "slug": "finland-gambling-licences-2026",
        "published_at": date(2026, 3, 1),
        "service_slug": "gambling",
        "source_name": "Gambling.com",
        "source_url": "https://www.gambling.com/news/finland-s-new-gambling-market-draws-about-50-licence-bids-before-2027-launch",
        "title": "Финляндия переходит от монополии к лицензиям: приём заявок на онлайн-гемблинг с 1 марта 2026",
        "title_en": "Finland moves from a monopoly to licensing: online gambling applications open on 1 March 2026",
        "excerpt": "С 1 марта 2026 года Национальная полиция Финляндии принимает заявки на лицензии. С 1 июля 2027 года частные операторы смогут работать на рынке онлайн-казино и беттинга.",
        "excerpt_en": "From 1 March 2026 the Finnish National Police Board accepts licence applications. From 1 July 2027 private operators may work in online casino and betting.",
        "content": (
            "С 1 марта 2026 года Национальная полиция Финляндии принимает заявки на лицензии на онлайн-гемблинг. Новый Закон об азартных играх отменяет государственную монополию: с 1 июля 2027 года рынок откроется для частных операторов.\n\n"
            "Лицензия покрывает онлайн-казино и беттинг. Отдельная лицензия на программное обеспечение станет доступна с июля 2027 года, а для работы с иностранными игорными компаниями предусмотрена лицензия на международное сотрудничество.\n\n"
            "Стоимость рассмотрения одной заявки составляет EUR 29 000. Эта плата взимается за каждую заявку независимо от решения регулятора. Регулятор ориентируется на срок рассмотрения около шести месяцев, но предупреждает, что неполные заявки будут рассматриваться дольше.\n\n"
            "Что важно учесть заранее: заявка подаётся только после подготовки полного пакета документов по бенефициарам, источникам средств, системам комплаенса и платёжной инфраструктуре; неполная заявка не ускоряет запуск, а задерживает его; структуру операционной компании лучше выстроить до подачи.\n\n"
            "Мы помогаем операторам оценить готовность к заявке, подготовить комплаенс-пакет и структуру компаний и сопровождать переписку с регулятором.\n\n"
            "Материал носит информационный характер и не является юридической консультацией."
        ),
        "content_en": (
            "From 1 March 2026 the Finnish National Police Board accepts applications for online gambling licences. The new Gambling Act ends the state monopoly: from 1 July 2027 the market opens to private operators.\n\n"
            "The licence covers online casino and betting services. A separate software licence becomes available from July 2027, and an international cooperation licence is provided for working with gambling companies outside Finland.\n\n"
            "The processing fee is EUR 29,000 per application. It is charged for every application, whether or not the regulator grants it. The regulator targets an average processing time of six months, but warns that incomplete applications will take longer.\n\n"
            "What to consider in advance: an application should be filed only once the full package is ready, covering beneficial owners, sources of funds, compliance systems and payment infrastructure; an incomplete application delays the launch rather than speeding it up; the operating company's structure is best set up before filing.\n\n"
            "We help operators assess readiness for an application, prepare the compliance package and company structure, and handle correspondence with the regulator.\n\n"
            "This article is for information only and is not legal advice."
        ),
    },
]


def run():
    with app.app_context():
        db.create_all()
        for data in SEED_NEWS:
            item = News.query.filter_by(slug=data["slug"]).first()
            if item is None:
                item = News(slug=data["slug"])
                db.session.add(item)
            for key, value in data.items():
                if key != "slug":
                    setattr(item, key, value)
        db.session.commit()
        print(f"Loaded {len(SEED_NEWS)} news articles.")


if __name__ == "__main__":
    run()
