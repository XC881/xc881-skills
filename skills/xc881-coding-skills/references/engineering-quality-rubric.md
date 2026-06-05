# Engineering Quality Rubric

A good change is:
- correct
- scoped
- readable
- locally consistent
- decoupled
- testable
- verified
- honest about assumptions

Low-quality signals:
- business rules scattered across UI/controllers/SQL/SDK callbacks
- circular dependencies
- core logic requires real infrastructure to test
- hidden side effects
- God object /万能 service /万能 utils
- unstable public contracts
- weak validation or swallowed errors
