def DuplicateJointHierarchy(actor, part, parentNode = None, level = 0):
    if isinstance(part, CharacterJoint):
        if parentNode:
			#create new characterJoint attached to parentNode
			new_joint = parentNode.attachNewNode() or parentNode.makeCharacterJoint(factoryParams??) ??
			#name it
			new_joint.setName(part.getName()+'N')
			#have it being an identity rotation matrix and no translation
			# new_joint.addLocalTransform(identity)??
			#detach part from parentNode and reparent it to new_joint
			part.reparenTo(new_joint)

    for child in part.getChildren():
        DuplicateJointHierarchy(actor, child, part, level + 1)


DuplicateJointHierarchy(actor, actor.getPartBundle('modelRoot'))
