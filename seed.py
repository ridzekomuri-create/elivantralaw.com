"""Run once to create the database and load the original 8 services into it.
Safe to re-run: it skips services whose slug already exists.

SEED_SERVICES is also imported by app.py to auto-seed an empty database on
startup (e.g. on hosts with an ephemeral filesystem) — that import must not
pull in Flask app creation, so `app` and `db` are only imported inside run()."""

SEED_SERVICES = [
    {
        "slug": "structuring",
        "icon": "globe",
        "title": "Международное структурирование бизнеса",
        "title_en": "International Business Structuring",
        "short": "Проектирование холдинговых и операционных структур под задачи роста, инвестиций и защиты активов.",
        "short_en": "Designing holding and operating structures for growth, investment and asset protection.",
        "text": "Разрабатываем архитектуру группы компаний с учётом юрисдикции бенефициаров, налоговой нагрузки, требований банков и будущих раундов инвестиций. Учитываем правила КИК, автоматический обмен информацией и требования economic substance.",
        "text_en": "We design the group's architecture with regard to the beneficiaries' jurisdiction, tax burden, banking requirements and future investment rounds, accounting for CFC rules, automatic exchange of information and economic substance requirements.",
        "points_raw": "Проектирование холдинговых и операционных цепочек\nВыбор юрисдикций с учётом CFC, ATAD и BEPS\nПодготовка к сделкам, инвестициям и IPO\nРеструктуризация существующих групп компаний",
        "points_en_raw": "Designing holding and operating chains\nJurisdiction selection with CFC, ATAD and BEPS in mind\nPreparing for deals, investment rounds and IPOs\nRestructuring existing corporate groups",
    },
    {
        "slug": "gambling",
        "icon": "dice",
        "title": "Юридическое сопровождение бизнеса в сфере азартных игр",
        "title_en": "Legal Support for Gambling Businesses",
        "short": "Лицензирование и комплаенс для операторов гемблинга и беттинга в ключевых регулируемых юрисдикциях.",
        "short_en": "Licensing and compliance for gambling and betting operators in key regulated jurisdictions.",
        "text": "Сопровождаем получение и продление игорных лицензий, выстраиваем комплаенс-политику под требования регуляторов, помогаем с платёжной инфраструктурой и взаимодействием с банками и PSP, работающими с высокорисковыми отраслями.",
        "text_en": "We support obtaining and renewing gambling licenses, build a compliance policy aligned with regulator requirements, and assist with payment infrastructure and relationships with banks and PSPs serving high-risk industries.",
        "points_raw": "Получение и продление игорных лицензий\nAML/KYC-политики и внутренний комплаенс\nСтруктурирование операционной компании и платежей\nСопровождение проверок и взаимодействия с регулятором",
        "points_en_raw": "Obtaining and renewing gambling licenses\nAML/KYC policies and internal compliance\nStructuring the operating company and payment flows\nSupport through regulator audits and inquiries",
    },
    {
        "slug": "blockchain",
        "icon": "chain",
        "title": "Юридическое сопровождение проектов в сфере блокчейна и криптовалют",
        "title_en": "Legal Support for Blockchain & Crypto Projects",
        "short": "Правовая база для криптопроектов: от токеномики и лицензирования VASP до сопровождения листинга.",
        "short_en": "A legal framework for crypto projects: from tokenomics and VASP licensing to listing support.",
        "text": "Помогаем криптопроектам и биржам работать в правовом поле: получение статуса VASP/CASP, разработка документации по токенам, структурирование фондов и DAO, юридическое сопровождение привлечения инвестиций и работы с биржами.",
        "text_en": "We help crypto projects and exchanges operate within the law: obtaining VASP/CASP status, drafting token documentation, structuring funds and DAOs, and providing legal support for fundraising and exchange listings.",
        "points_raw": "Лицензирование VASP / CASP и регистрация в MiCA-юрисдикциях\nТокеномика, whitepaper и юридическая документация\nСтруктурирование криптофондов и DAO\nDue diligence перед листингом и привлечением инвестиций",
        "points_en_raw": "VASP / CASP licensing and registration in MiCA jurisdictions\nTokenomics, whitepapers and legal documentation\nStructuring crypto funds and DAOs\nDue diligence ahead of listings and fundraising",
    },
    {
        "slug": "registration",
        "icon": "seal",
        "title": "Регистрация и сопровождение бизнеса за рубежом",
        "title_en": "Company Registration & Support Abroad",
        "short": "Регистрация компаний, номинальный сервис, корпоративное администрирование и годовое сопровождение.",
        "short_en": "Company incorporation, nominee services, corporate administration and annual support.",
        "text": "Открываем компании в более чем 40 юрисдикциях под конкретную бизнес-задачу, готовим корпоративный пакет документов, обеспечиваем зарегистрированный офис и агента, ведём текущее корпоративное администрирование и отчётность.",
        "text_en": "We incorporate companies in 40+ jurisdictions tailored to the specific business task, prepare the corporate document package, provide a registered office and agent, and handle ongoing corporate administration and reporting.",
        "points_raw": "Регистрация компаний в Европе, Азии, на Ближнем Востоке и в оффшорных зонах\nЗарегистрированный офис, агент, номинальный сервис\nКорпоративное администрирование и ежегодная отчётность\nПолучение необходимых разрешений и лицензий",
        "points_en_raw": "Company registration across Europe, Asia, the Middle East and offshore zones\nRegistered office, agent and nominee services\nCorporate administration and annual reporting\nObtaining the required permits and licenses",
    },
    {
        "slug": "banking",
        "icon": "bank",
        "title": "Открытие банковских и PSP-счетов",
        "title_en": "Opening Bank and PSP Accounts",
        "short": "Подбор банков и платёжных провайдеров, подготовка пакета документов и сопровождение комплаенс-проверки.",
        "short_en": "Selecting banks and payment providers, preparing the package and managing the compliance review.",
        "text": "Подбираем банки и PSP под профиль бизнеса и страну бенефициара, готовим пакет документов и бизнес-обоснование, сопровождаем прохождение комплаенса и коммуникацию с банком вплоть до открытия и активации счёта.",
        "text_en": "We select banks and PSPs that fit the business profile and the beneficiary's country, prepare the document package and business rationale, and manage the bank's compliance review through to account opening and activation.",
        "points_raw": "Подбор банков и PSP под отрасль и юрисдикцию\nПодготовка пакета документов и структуры KYC\nСопровождение комплаенс-проверки банка\nМультивалютные и мерчант-счета для онлайн-бизнеса",
        "points_en_raw": "Bank and PSP selection by industry and jurisdiction\nPreparing documentation and the KYC structure\nManaging the bank's compliance review\nMulti-currency and merchant accounts for online business",
    },
    {
        "slug": "due-diligence",
        "icon": "search",
        "title": "Due Diligence и структурирование сделок",
        "title_en": "Due Diligence & Deal Structuring",
        "short": "Юридическая и финансовая проверка контрагентов, активов и структур перед сделкой.",
        "short_en": "Legal and financial review of counterparties, assets and structures ahead of a deal.",
        "text": "Проводим правовую и репутационную проверку контрагентов, активов и корпоративных структур, выявляем риски до подписания сделки и разрабатываем оптимальную структуру транзакции — от NDA и term sheet до закрытия сделки.",
        "text_en": "We conduct legal and reputational checks on counterparties, assets and corporate structures, surface risks before signing, and design the optimal transaction structure — from NDA and term sheet through to closing.",
        "points_raw": "Юридический и налоговый due diligence\nПроверка бенефициаров и репутационные риски\nСтруктурирование M&A и инвестиционных сделок\nДоговорное сопровождение до закрытия сделки",
        "points_en_raw": "Legal and tax due diligence\nBeneficiary checks and reputational risk review\nStructuring M&A and investment deals\nContract support through to deal closing",
    },
    {
        "slug": "tax-legal",
        "icon": "scale",
        "title": "Налоговый и юридический консалтинг",
        "title_en": "Tax & Legal Consulting",
        "short": "Налоговое планирование, оптимизация структуры и правовое сопровождение операционной деятельности.",
        "short_en": "Tax planning, structure optimization and legal support for day-to-day operations.",
        "text": "Консультируем по международному налогообложению, применению соглашений об избежании двойного налогообложения, подготовке transfer pricing документации и текущим юридическим вопросам ведения бизнеса в разных юрисдикциях.",
        "text_en": "We advise on international taxation, the application of double tax treaties, transfer pricing documentation, and the day-to-day legal matters of running a business across jurisdictions.",
        "points_raw": "Международное налоговое планирование и DTT\nTransfer pricing и подготовка обосновывающей документации\nЮридическое сопровождение операционной деятельности\nПравовые заключения и консультации по запросу",
        "points_en_raw": "International tax planning and double tax treaties\nTransfer pricing and supporting documentation\nLegal support for operating activities\nLegal opinions and consultations on request",
    },
    {
        "slug": "full-support",
        "icon": "laurel",
        "title": "Комплексное юридическое сопровождение бизнеса",
        "title_en": "Comprehensive Legal Support for Business",
        "short": "Функция внешнего юридического департамента: от регистрации до ежедневных правовых вопросов.",
        "short_en": "Functioning as your outside legal department — from registration to everyday legal matters.",
        "text": "Берём на себя роль постоянного юридического партнёра: сопровождаем компанию на всех этапах — от регистрации и лицензирования до договорной работы, комплаенса и представления интересов перед контрагентами и регуляторами.",
        "text_en": "We act as your standing legal partner, supporting the company at every stage — from registration and licensing to contract work, compliance, and representing your interests before counterparties and regulators.",
        "points_raw": "Постоянное юридическое сопровождение на аутсорсе\nДоговорная работа и правовая экспертиза сделок\nКомплаенс, корпоративное управление, отчётность\nЕдиная точка контакта по всем юрисдикциям присутствия",
        "points_en_raw": "Ongoing outsourced legal support\nContract work and legal review of deals\nCompliance, corporate governance and reporting\nA single point of contact across all jurisdictions",
    },
]


def run():
    from app import app
    from models import Service, db

    with app.app_context():
        db.create_all()
        existing = {s.slug for s in Service.query.all()}
        added = 0
        for i, data in enumerate(SEED_SERVICES):
            if data["slug"] in existing:
                continue
            db.session.add(Service(sort_order=i, **data))
            added += 1
        db.session.commit()
        print(f"Seed complete. Added {added} new service(s). Total: {Service.query.count()}.")


if __name__ == "__main__":
    run()
