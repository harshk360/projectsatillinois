import math

def getVectorKeywordIndex(skills):
    VectorIndex = {}
    offset = 0
    for skill in skills:
        VectorIndex[skill.name] = offset
        offset += 1
    return VectorIndex

def makeSkillVector(vectorKeywordIndex, skills):
    vector = [0] * len(vectorKeywordIndex)
    for skill in skills:
        vector[vectorKeywordIndex[skill.name]] += 1
    return vector

def search(user, projects):
    skills = user.skills()
    vectorKeywordIndex = getVectorKeywordIndex(skills)
    userSkillVector = makeSkillVector(vectorKeywordIndex, skills)
    scoreList = []
    for project in projects:
        projectSkillVector = makeSkillVector(vectorKeywordIndex, project.skills)
        score = cosine(projectSkillVector, userSkillVector)
        bundle = {}
        bundle['projectId'] = project.id
        bundle['score'] = score
        scoreList.append(bundle)
    return scoreList

def cosine(vector1, vector2):
    return float(dot(vector1,vector2) / (norm(vector1) * norm(vector2)))

def dot(vector1, vector2):
    output = 0
    for dimension, value in enumerate(vector1):
        output += vector1[dimension]*vector2[dimension]
    return output

def norm(vector1):
    output = 0
    for value in vector1:
        output += value*value
    return math.sqrt(output)
