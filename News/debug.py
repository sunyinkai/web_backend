#将文件转换为json
# return JsonResponse(obj, safe=False)
# return HttpResponse(to_json(posts),content_type='application/json')
# return HttpResponse(json.dumps(all_message),content_type='application/json')

# comments = Comment.objects.filter(post__id=news_id).select_related()  # 将指定id号下的所有comment都找出来
# for comment in comments:

#Comment.objects.filter 与 Comment.objects.get 的区别