"""One-off script to seed 5 sample courses with modules and quizzes, for demo
purposes. Run manually: python -m scripts.seed_sample_courses

Idempotent: skips any course whose title already exists, so it's safe to
re-run after adding more courses to this list.

Certificates are never seeded directly — they're auto-issued the moment a
learner passes every quiz in a course (see certificate_service). Log in as a
learner and pass all quizzes in a course to see one issued for real.
"""

from app.core.database import Base, SessionLocal, engine
from app.models.assessment import Question, Quiz, SkillCategory
from app.models.course import Course, Module

COURSES = [
    {
        "title": "Git & GitHub Essentials",
        "description": "Version control fundamentals: commits, branches, merges, pull requests, and collaborative workflows on GitHub.",
        "skill_category": SkillCategory.digital_literacy,
        "modules": [
            {
                "title": "Git Basics",
                "content": (
                    "Git is a distributed version control system that tracks changes to files over time. "
                    "A repository (repo) is a project's full history, stored locally and optionally on a remote host like GitHub. "
                    "The core workflow is: edit files, `git add` to stage changes, `git commit` to save a snapshot with a message, "
                    "and `git push` to send commits to a remote repository. `git status` shows what's changed and staged; "
                    "`git log` shows commit history. Unlike a simple backup, every commit is a full point-in-time snapshot you can "
                    "return to, and Git tracks changes by content, not by file name, so renamed or moved files are still tracked correctly."
                ),
            },
            {
                "title": "Branching, Merging, and Pull Requests",
                "content": (
                    "A branch is an independent line of development, usually created off `main` with `git branch` or `git checkout -b`. "
                    "Branches let multiple people work in parallel without stepping on each other's changes. `git merge` combines a "
                    "branch's changes back into another branch; if the same lines were changed on both sides, Git raises a merge conflict "
                    "that a human must resolve manually. On GitHub, a pull request (PR) is a request to merge one branch into another, "
                    "and it's also where code review happens — teammates comment on specific lines, request changes, and approve before "
                    "the PR is merged. `git fetch` downloads remote changes without merging them; `git pull` does fetch + merge in one step. "
                    "A `.gitignore` file tells Git which files (build artifacts, secrets, dependencies) to never track."
                ),
            },
        ],
        "quiz": {
            "title": "Git & GitHub Basics",
            "pass_threshold_pct": 70,
            "questions": [
                {
                    "text": "What does `git commit` do?",
                    "options": [
                        "Uploads the repository to GitHub",
                        "Saves a snapshot of staged changes with a message",
                        "Deletes uncommitted changes",
                        "Creates a new branch",
                    ],
                    "correct_index": 1,
                },
                {
                    "text": "What is a merge conflict?",
                    "options": [
                        "An error that occurs when you push to the wrong branch",
                        "A warning that a repository is out of disk space",
                        "When the same lines were changed differently on both branches being merged, requiring manual resolution",
                        "A permission error on GitHub",
                    ],
                    "correct_index": 2,
                },
                {
                    "text": "On GitHub, what is a pull request primarily used for?",
                    "options": [
                        "Deleting a branch",
                        "Proposing and reviewing a merge of one branch into another",
                        "Downloading the repo to your machine",
                        "Renaming the repository",
                    ],
                    "correct_index": 1,
                },
                {
                    "text": "What's the difference between `git fetch` and `git pull`?",
                    "options": [
                        "They are identical commands",
                        "`git fetch` downloads remote changes without merging; `git pull` fetches and merges in one step",
                        "`git fetch` deletes local changes; `git pull` does not",
                        "`git fetch` only works on GitHub, `git pull` works everywhere",
                    ],
                    "correct_index": 1,
                },
                {
                    "text": "What is the purpose of a `.gitignore` file?",
                    "options": [
                        "To list commit messages",
                        "To specify files/folders Git should never track (e.g. build artifacts, secrets)",
                        "To store your GitHub password",
                        "To merge branches automatically",
                    ],
                    "correct_index": 1,
                },
            ],
        },
    },
    {
        "title": "AI Fundamentals",
        "description": "Core concepts behind modern artificial intelligence: what AI is, how machine learning fits in, and how large language models work.",
        "skill_category": SkillCategory.problem_solving,
        "modules": [
            {
                "title": "What Is AI?",
                "content": (
                    "Artificial intelligence (AI) is the broad field of building systems that perform tasks normally requiring human "
                    "intelligence — recognizing images, understanding language, making decisions. Machine learning (ML) is a subset of AI "
                    "where systems learn patterns from data rather than following explicitly hand-coded rules. Deep learning is a subset of "
                    "ML that uses neural networks with many layers, and it's responsible for most recent AI breakthroughs, including image "
                    "recognition and language models. AI systems are generally categorized as narrow AI (built for one specific task, like "
                    "spam filtering or chess) versus the hypothetical general AI (human-level intelligence across any task) — every AI system "
                    "in production use today is narrow AI, despite marketing language that sometimes implies otherwise."
                ),
            },
            {
                "title": "How Large Language Models Work",
                "content": (
                    "A large language model (LLM) like GPT or Claude is trained on massive amounts of text to predict the next word (technically, "
                    "the next 'token') in a sequence, given everything before it. Through this simple objective, repeated across billions of "
                    "examples, the model learns grammar, facts, and reasoning patterns embedded in its training data. A 'prompt' is the input text "
                    "you give the model; the model generates a response by repeatedly predicting the most likely next token. LLMs don't have "
                    "real-time knowledge or true understanding — they produce statistically plausible text, which is why they can 'hallucinate' "
                    "confident-sounding but false information. Techniques like retrieval-augmented generation (RAG) address this by giving the "
                    "model relevant real documents to reference alongside its prompt, rather than relying purely on what it memorized during training."
                ),
            },
        ],
        "quiz": {
            "title": "AI Fundamentals Quiz",
            "pass_threshold_pct": 70,
            "questions": [
                {
                    "text": "How does machine learning differ from traditional hand-coded software?",
                    "options": [
                        "ML systems learn patterns from data instead of following explicit rules",
                        "ML systems are always faster than hand-coded rules",
                        "ML doesn't require any data",
                        "There is no meaningful difference",
                    ],
                    "correct_index": 0,
                },
                {
                    "text": "What is deep learning?",
                    "options": [
                        "A synonym for artificial intelligence in general",
                        "A subset of machine learning using multi-layer neural networks",
                        "A method for manually writing rules for a computer",
                        "A type of database",
                    ],
                    "correct_index": 1,
                },
                {
                    "text": "What is 'narrow AI'?",
                    "options": [
                        "AI that can perform any task a human can, at human level",
                        "AI trained on a small dataset",
                        "AI built to perform one specific task well, which describes all AI systems in production today",
                        "AI that only runs on small devices",
                    ],
                    "correct_index": 2,
                },
                {
                    "text": "What does an LLM fundamentally do when generating text?",
                    "options": [
                        "Looks up pre-written answers in a database",
                        "Repeatedly predicts the most likely next token given everything before it",
                        "Searches the internet in real time",
                        "Runs a fixed decision tree",
                    ],
                    "correct_index": 1,
                },
                {
                    "text": "What problem does retrieval-augmented generation (RAG) address?",
                    "options": [
                        "It makes models generate text faster",
                        "It reduces hallucination by giving the model real reference documents alongside the prompt",
                        "It trains the model from scratch",
                        "It compresses the model to run on smaller hardware",
                    ],
                    "correct_index": 1,
                },
            ],
        },
    },
    {
        "title": "Forward Deployed Engineering (FDE)",
        "description": "What a forward deployed engineer does: embedding with clients, rapid prototyping, and translating real-world workflows into working software.",
        "skill_category": SkillCategory.workplace_professionalism,
        "modules": [
            {
                "title": "The FDE Role",
                "content": (
                    "A forward deployed engineer (FDE) works directly at or with a client's site, rather than purely from a central "
                    "product team, to understand the client's actual workflows and build software that fits their real operational needs. "
                    "The role blends software engineering, product thinking, and client-facing communication: FDEs write real production "
                    "code, but they also run workshops, gather requirements from domain experts (who are often not engineers themselves), "
                    "and rapidly iterate based on direct feedback in the room. This is different from a traditional product engineer, who "
                    "builds for a broad, general user base based on aggregated feedback and roadmap planning — an FDE typically builds for "
                    "one client's specific, sometimes messy, real-world context first, and generalizes patterns back into the core product later."
                ),
            },
            {
                "title": "Rapid Prototyping and Client Trust",
                "content": (
                    "Speed and iteration are central to FDE work: a common pattern is building a working prototype within days, showing it "
                    "to the client's domain experts, and rapidly incorporating their corrections — because domain experts often can't fully "
                    "articulate their workflow in the abstract, but can immediately spot what's wrong once they see something concrete. This "
                    "requires strong communication skills alongside engineering skill: explaining technical tradeoffs in plain language, "
                    "setting realistic expectations, and building trust with people who are not engineers and may be skeptical of new tooling. "
                    "FDEs also need to recognize when a client-specific solution reveals a broader pattern worth building into the core product, "
                    "versus when it's genuinely a one-off need — conflating the two either bloats the core product with edge cases or leaves "
                    "every client reinventing the same solution."
                ),
            },
        ],
        "quiz": {
            "title": "FDE Fundamentals Quiz",
            "pass_threshold_pct": 70,
            "questions": [
                {
                    "text": "What primarily distinguishes an FDE from a traditional product engineer?",
                    "options": [
                        "FDEs never write production code",
                        "FDEs build directly for one client's real workflow and context, often on-site, rather than a general user base",
                        "FDEs only do requirements gathering, never engineering",
                        "There is no real difference",
                    ],
                    "correct_index": 1,
                },
                {
                    "text": "Why is rapid prototyping especially effective with domain experts?",
                    "options": [
                        "Domain experts prefer written specs over demos",
                        "It's faster to build than to talk to the client at all",
                        "Domain experts often can't fully describe their workflow abstractly, but can immediately spot issues in a concrete prototype",
                        "Prototypes never need to be revised",
                    ],
                    "correct_index": 2,
                },
                {
                    "text": "Besides engineering skill, what is central to FDE work?",
                    "options": [
                        "Avoiding client contact as much as possible",
                        "Communication and trust-building with non-engineer stakeholders",
                        "Only working on backend infrastructure",
                        "Following a fixed roadmap with no client input",
                    ],
                    "correct_index": 1,
                },
                {
                    "text": "What risk does an FDE need to watch for when a client-specific solution seems broadly useful?",
                    "options": [
                        "Nothing — always generalize every solution immediately",
                        "Conflating a genuine one-off need with a broadly reusable pattern, which can bloat the core product or fragment solutions across clients",
                        "That the client will not want a demo",
                        "That the solution will be too slow to build",
                    ],
                    "correct_index": 1,
                },
                {
                    "text": "What does 'embedding with a client' mean in an FDE context?",
                    "options": [
                        "Installing tracking software on client devices",
                        "Working directly at or closely with the client's site/team to understand their actual operational needs",
                        "Embedding client logos in the product UI",
                        "Working exclusively remotely with no client contact",
                    ],
                    "correct_index": 1,
                },
            ],
        },
    },
    {
        "title": "Machine Learning Foundations",
        "description": "Supervised vs. unsupervised learning, overfitting, and how models are trained, validated, and evaluated.",
        "skill_category": SkillCategory.problem_solving,
        "modules": [
            {
                "title": "Supervised and Unsupervised Learning",
                "content": (
                    "Supervised learning trains a model on labeled data — input-output pairs where the correct answer is already known, "
                    "like emails labeled 'spam' or 'not spam'. The model learns to map new inputs to the correct output. Common tasks are "
                    "classification (predicting a category) and regression (predicting a number). Unsupervised learning works on unlabeled "
                    "data, finding structure without being told the answer — clustering similar items together, or reducing data to its most "
                    "important dimensions. A classic example is customer segmentation: grouping customers by purchasing behavior without "
                    "predefined categories. Reinforcement learning is a third paradigm, where an agent learns by taking actions in an "
                    "environment and receiving rewards or penalties, gradually learning a strategy that maximizes reward over time."
                ),
            },
            {
                "title": "Overfitting, Validation, and Evaluation",
                "content": (
                    "Overfitting happens when a model learns the training data too specifically — including its noise and quirks — so it "
                    "performs well on training data but poorly on new, unseen data. This is why data is typically split into a training set "
                    "(used to fit the model) and a separate test set (used only to evaluate final performance, never to adjust the model). A "
                    "validation set is often held out separately from both, used during development to tune model settings (hyperparameters) "
                    "without contaminating the final test evaluation. For classification tasks, accuracy alone can be misleading on imbalanced "
                    "data (e.g. 99% of emails are not spam, so a model that always predicts 'not spam' gets 99% accuracy while being useless) — "
                    "precision, recall, and F1 score are used instead to capture how well a model actually identifies the minority class."
                ),
            },
        ],
        "quiz": {
            "title": "ML Foundations Quiz",
            "pass_threshold_pct": 70,
            "questions": [
                {
                    "text": "What defines supervised learning?",
                    "options": [
                        "The model is trained on unlabeled data",
                        "The model is trained on labeled input-output pairs",
                        "The model receives rewards and penalties from an environment",
                        "The model requires no training data at all",
                    ],
                    "correct_index": 1,
                },
                {
                    "text": "What is a typical use case for unsupervised learning?",
                    "options": [
                        "Predicting house prices from labeled sale data",
                        "Classifying labeled spam vs. not-spam emails",
                        "Clustering customers into segments without predefined categories",
                        "Playing a game to maximize a score via trial and error",
                    ],
                    "correct_index": 2,
                },
                {
                    "text": "What is overfitting?",
                    "options": [
                        "When a model trains too quickly",
                        "When a model learns training data (including its noise) too specifically and performs poorly on new data",
                        "When a model uses too little training data",
                        "When a model has too few parameters",
                    ],
                    "correct_index": 1,
                },
                {
                    "text": "Why is accuracy alone often misleading on imbalanced datasets?",
                    "options": [
                        "Accuracy is always 100% on imbalanced data",
                        "A model that always predicts the majority class can score high accuracy while being useless at detecting the minority class",
                        "Accuracy can only be computed on balanced data",
                        "Imbalanced data makes accuracy impossible to calculate",
                    ],
                    "correct_index": 1,
                },
                {
                    "text": "What is the purpose of a held-out test set?",
                    "options": [
                        "To train the model faster",
                        "To evaluate final model performance on data never used to fit or tune the model",
                        "To increase the size of the training data",
                        "To replace the need for a validation set",
                    ],
                    "correct_index": 1,
                },
            ],
        },
    },
    {
        "title": "Software Development Engineering (SDE)",
        "description": "Core practices of professional software engineering: version control workflows, testing, code review, and writing maintainable code.",
        "skill_category": SkillCategory.problem_solving,
        "modules": [
            {
                "title": "Writing Maintainable Code",
                "content": (
                    "Maintainable code is code that other engineers (including your future self) can understand, modify, and extend safely. "
                    "Key practices include: clear naming that describes intent rather than implementation detail, functions that do one thing "
                    "and are small enough to reason about at a glance, and avoiding premature abstraction — building a general-purpose solution "
                    "before you actually have more than one concrete use case tends to add complexity without real benefit. Comments should "
                    "explain *why* something non-obvious is done, not restate *what* the code already says. Technical debt refers to the "
                    "implied cost of quick, expedient solutions that will require more work later — it isn't inherently bad, but unmanaged "
                    "technical debt compounds and slows every future change, so professional teams track and deliberately pay it down."
                ),
            },
            {
                "title": "Testing and Code Review",
                "content": (
                    "Automated tests verify that code behaves correctly and continue to catch regressions as the codebase changes. Unit tests "
                    "check a single function or component in isolation; integration tests check that multiple components work correctly "
                    "together; end-to-end tests simulate a real user flow through the whole system. A test suite gives engineers the confidence "
                    "to refactor and change code without manually re-verifying everything by hand. Code review is the practice of having another "
                    "engineer read and critique a proposed change before it's merged — it catches bugs a single author might miss, spreads "
                    "knowledge of the codebase across the team, and enforces consistency. Continuous integration (CI) automatically runs a "
                    "project's tests (and often linters/build checks) on every proposed change, so problems are caught before merge rather than "
                    "discovered in production."
                ),
            },
        ],
        "quiz": {
            "title": "SDE Fundamentals Quiz",
            "pass_threshold_pct": 70,
            "questions": [
                {
                    "text": "What is technical debt?",
                    "options": [
                        "A bug that crashes the application",
                        "The implied future cost of a quick, expedient solution chosen now over a more thorough one",
                        "Money owed to a software vendor",
                        "Code that has no tests",
                    ],
                    "correct_index": 1,
                },
                {
                    "text": "What's a good rule of thumb about premature abstraction?",
                    "options": [
                        "Always build the most general solution possible from the start",
                        "Avoid building generalized solutions before you have more than one concrete use case, since it adds complexity without real benefit yet",
                        "Abstraction should never be used in production code",
                        "Abstractions should always be added after code review",
                    ],
                    "correct_index": 1,
                },
                {
                    "text": "What does a unit test check?",
                    "options": [
                        "A full user flow through the entire system",
                        "A single function or component in isolation",
                        "The deployment pipeline configuration",
                        "Whether the code compiles at all",
                    ],
                    "correct_index": 1,
                },
                {
                    "text": "What is the main benefit of code review?",
                    "options": [
                        "It replaces the need for automated tests",
                        "It catches bugs a single author might miss, spreads codebase knowledge, and enforces consistency",
                        "It slows down all development with no benefit",
                        "It is only useful for junior engineers",
                    ],
                    "correct_index": 1,
                },
                {
                    "text": "What does continuous integration (CI) do?",
                    "options": [
                        "Manually deploys code once a week",
                        "Automatically runs tests/checks on every proposed change so problems are caught before merge",
                        "Writes code automatically",
                        "Replaces the need for a version control system",
                    ],
                    "correct_index": 1,
                },
            ],
        },
    },
]


def seed_sample_courses():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        for course_data in COURSES:
            existing = db.query(Course).filter(Course.title == course_data["title"]).first()
            if existing:
                print(f"Skipping (already exists): {course_data['title']}")
                continue

            course = Course(title=course_data["title"], description=course_data["description"])
            db.add(course)
            db.flush()

            for idx, module_data in enumerate(course_data["modules"]):
                db.add(
                    Module(
                        course_id=course.id,
                        title=module_data["title"],
                        content=module_data["content"],
                        order_index=idx,
                    )
                )

            quiz_data = course_data["quiz"]
            quiz = Quiz(
                course_id=course.id,
                title=quiz_data["title"],
                pass_threshold_pct=quiz_data["pass_threshold_pct"],
                adaptive=False,
                skill_category=course_data["skill_category"],
            )
            db.add(quiz)
            db.flush()

            for idx, q in enumerate(quiz_data["questions"]):
                db.add(
                    Question(
                        quiz_id=quiz.id,
                        text=q["text"],
                        options=q["options"],
                        correct_index=q["correct_index"],
                        order_index=idx,
                    )
                )

            db.commit()
            print(f"Created: {course_data['title']} ({len(course_data['modules'])} modules, {len(quiz_data['questions'])} quiz questions)")
    finally:
        db.close()


if __name__ == "__main__":
    seed_sample_courses()
